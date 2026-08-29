from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.repositories import require_user
from app.db import get_db
from app.models import PullRequest, Repository, User
from app.services.risk import predict_risk

router = APIRouter(tags=["pull-requests"])


@router.get("/repositories/{repository_id}/pull-requests")
def list_pull_requests(repository_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)) -> list[dict]:
    repository = db.scalar(select(Repository).where(Repository.id == repository_id, Repository.owner_id == user.id, Repository.is_connected.is_(True)))
    if repository is None:
        raise HTTPException(status_code=404, detail="Connected repository not found")
    return [{"id": pr.id, "number": pr.github_number, "title": pr.title, "state": pr.state, "risk": predict_risk(pr)} for pr in db.scalars(select(PullRequest).where(PullRequest.repository_id == repository.id).order_by(PullRequest.created_at.desc())).all()]


@router.get("/pull-requests/{pull_request_id}/risk")
def pull_request_risk(pull_request_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)) -> dict:
    pr = db.scalar(select(PullRequest).join(Repository).where(PullRequest.id == pull_request_id, Repository.owner_id == user.id))
    if pr is None:
        raise HTTPException(status_code=404, detail="Pull request not found")
    return predict_risk(pr)
