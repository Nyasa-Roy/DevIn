from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.github import GitHubClient
from app.models import Repository, User
from app.security import decrypt_token

router = APIRouter(prefix="/repositories", tags=["repositories"])


def require_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_id = request.session.get("user_id")
    user = db.get(User, user_id) if user_id else None
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


async def github_for(user: User) -> GitHubClient:
    if not user.github_token_encrypted:
        raise HTTPException(status_code=400, detail="GitHub account has no usable access token")
    return GitHubClient(decrypt_token(user.github_token_encrypted))


@router.get("")
async def list_repositories(user: User = Depends(require_user), db: Session = Depends(get_db)) -> list[dict]:
    client = await github_for(user)
    try:
        accessible = await client.repositories()
    finally:
        await client.close()
    connected = {repo.github_id: repo for repo in db.scalars(select(Repository).where(Repository.owner_id == user.id)).all()}
    return [{"id": item["id"], "name": item["name"], "full_name": item["full_name"], "html_url": item["html_url"], "private": item["private"], "connected": item["id"] in connected} for item in accessible]


@router.post("/{github_id}/connect", status_code=status.HTTP_201_CREATED)
async def connect_repository(github_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)) -> dict:
    client = await github_for(user)
    try:
        accessible = await client.repositories()
        item = next((repo for repo in accessible if repo["id"] == github_id), None)
        if item is None:
            raise HTTPException(status_code=404, detail="Repository not found or inaccessible")
    finally:
        await client.close()
    repository = db.scalar(select(Repository).where(Repository.github_id == github_id, Repository.owner_id == user.id))
    if repository is None:
        repository = Repository(github_id=github_id, owner_id=user.id, name=item["name"], full_name=item["full_name"], html_url=item["html_url"], default_branch=item.get("default_branch") or "main")
        db.add(repository)
    else:
        repository.is_connected = True
    db.commit()
    db.refresh(repository)
    return {"id": repository.id, "github_id": repository.github_id, "full_name": repository.full_name, "connected": repository.is_connected}


@router.delete("/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
def disconnect_repository(repository_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)) -> None:
    repository = db.scalar(select(Repository).where(Repository.id == repository_id, Repository.owner_id == user.id))
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    repository.is_connected = False
    db.commit()


@router.post("/{repository_id}/sync")
async def sync_repository(repository_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)) -> dict:
    repository = db.scalar(select(Repository).where(Repository.id == repository_id, Repository.owner_id == user.id, Repository.is_connected.is_(True)))
    if repository is None:
        raise HTTPException(status_code=404, detail="Connected repository not found")
    client = await github_for(user)
    try:
        snapshot = await client.repository_snapshot(repository.full_name, repository.default_branch)
    finally:
        await client.close()
    repository.synced_at = datetime.now(timezone.utc)
    db.commit()
    return {"repository_id": repository.id, "status": "completed", "counts": {key: len(value) for key, value in snapshot.items() if isinstance(value, list)}, "synced_at": repository.synced_at}
