from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.repositories import require_user
from app.db import get_db
from app.models import Repository, User
from app.services.anomalies import repository_anomalies
from app.services.search import search_files

router = APIRouter(prefix="/repositories", tags=["intelligence"])


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)


def owned_repository(repository_id: int, user: User, db: Session) -> Repository:
    repository = db.scalar(select(Repository).where(Repository.id == repository_id, Repository.owner_id == user.id, Repository.is_connected.is_(True)))
    if repository is None:
        raise HTTPException(status_code=404, detail="Connected repository not found")
    return repository


@router.get("/{repository_id}/anomalies")
def anomalies(repository_id: int, user: User = Depends(require_user), db: Session = Depends(get_db)) -> dict:
    owned_repository(repository_id, user, db)
    return {"anomalies": repository_anomalies(db, repository_id)}


@router.post("/{repository_id}/search")
def semantic_search(repository_id: int, request: SearchRequest, user: User = Depends(require_user), db: Session = Depends(get_db)) -> dict:
    owned_repository(repository_id, user, db)
    return {"query": request.query, "results": search_files(db, repository_id, request.query, request.limit), "retrieval": "lexical-baseline"}
