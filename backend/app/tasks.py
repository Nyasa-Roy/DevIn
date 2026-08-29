import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from app.db import SessionLocal
from app.github import GitHubClient
from app.models import Repository, SyncJob, User
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
