import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from app.db import SessionLocal
from app.github import GitHubClient
from app.models import Commit, Issue, PullRequest, Repository, SyncJob, User
from app.queue import celery_app
from app.security import decrypt_token


@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def sync_repository_task(self, job_id: str) -> dict:
    return asyncio.run(_sync_repository(job_id))


async def _sync_repository(job_id: str) -> dict:
    db = SessionLocal()
    job = db.get(SyncJob, job_id)
    if job is None:
        db.close()
        raise ValueError("Sync job not found")
    job.status = "running"
    db.commit()
    client = None
    try:
        repository = db.get(Repository, job.repository_id)
        user = db.get(User, repository.owner_id) if repository else None
        if repository is None or user is None or not user.github_token_encrypted:
            raise ValueError("Repository credentials are unavailable")
        client = GitHubClient(decrypt_token(user.github_token_encrypted))
        snapshot = await client.repository_snapshot(repository.full_name, repository.default_branch)
        _persist_snapshot(db, repository.id, snapshot)
        repository.synced_at = datetime.now(timezone.utc)
        job.status = "completed"
        job.completed_at = datetime.now(timezone.utc)
        db.commit()
        return {"job_id": job.id, "status": job.status, "counts": {key: len(value) for key, value in snapshot.items() if isinstance(value, list)}}
    except Exception as exc:
        job.status = "failed"
        job.error = str(exc)
        db.commit()
        raise
    finally:
        if client:
            await client.close()
        db.close()


def _parse_datetime(value: str | None):
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _persist_snapshot(db, repository_id: int, snapshot: dict) -> None:
    for item in snapshot.get("commits", []):
        sha = item.get("sha")
        if not sha or db.query(Commit).filter_by(repository_id=repository_id, sha=sha).first():
            continue
        author = item.get("author") or {}
        commit_data = item.get("commit") or {}
        db.add(Commit(repository_id=repository_id, sha=sha, author_login=author.get("login"), message=(commit_data.get("message") or "").splitlines()[0], committed_at=_parse_datetime((commit_data.get("author") or {}).get("date"))))
    for item in snapshot.get("pull_requests", []):
        number = item.get("number")
        if number is None:
            continue
        record = db.query(PullRequest).filter_by(repository_id=repository_id, github_number=number).first()
        if record is None:
            db.add(PullRequest(repository_id=repository_id, github_number=number, title=item.get("title", ""), state=item.get("state", "open"), author_login=(item.get("user") or {}).get("login"), created_at=_parse_datetime(item.get("created_at")), merged_at=_parse_datetime(item.get("merged_at"))))
    for item in snapshot.get("issues", []):
        number = item.get("number")
        if number is None or db.query(Issue).filter_by(repository_id=repository_id, github_number=number).first():
            continue
        db.add(Issue(repository_id=repository_id, github_number=number, title=item.get("title", ""), state=item.get("state", "open"), created_at=_parse_datetime(item.get("created_at"))))
