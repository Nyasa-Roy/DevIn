from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PullRequest


def repository_anomalies(db: Session, repository_id: int) -> list[dict]:
    pull_requests = db.scalars(select(PullRequest).where(PullRequest.repository_id == repository_id)).all()
    sizes = sorted(pr.additions + pr.deletions for pr in pull_requests)
    if len(sizes) < 4:
        return []
    median = sizes[len(sizes) // 2]
    threshold = max(400, median * 3)
    return [{"pull_request_id": pr.id, "github_number": pr.github_number, "type": "large_pull_request", "value": pr.additions + pr.deletions, "baseline": median, "message": f"PR #{pr.github_number} is unusually large for this repository"} for pr in pull_requests if pr.additions + pr.deletions > threshold]
