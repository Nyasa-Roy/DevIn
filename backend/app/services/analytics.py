from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Commit, Issue, PullRequest, Repository


def repository_metrics(db: Session, repository: Repository, days: int = 30) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    commits = []
    for item in db.scalars(select(Commit).where(Commit.repository_id == repository.id)).all():
        committed_at = item.committed_at.replace(tzinfo=timezone.utc) if item.committed_at and item.committed_at.tzinfo is None else item.committed_at
        if not committed_at or committed_at >= cutoff:
            commits.append(item)
    prs = db.scalars(select(PullRequest).where(PullRequest.repository_id == repository.id)).all()
    issues = db.scalars(select(Issue).where(Issue.repository_id == repository.id)).all()
    open_prs = sum(pr.state == "open" for pr in prs)
    merged_prs = sum(pr.merged_at is not None for pr in prs)
    open_issues = sum(issue.state == "open" for issue in issues)
    average_pr_size = round(sum(pr.additions + pr.deletions for pr in prs) / len(prs), 1) if prs else 0
    health = max(0, min(100, 70 + min(20, len(commits)) - min(15, open_prs) - min(10, open_issues // 10)))
    return {"repository_id": repository.id, "period_days": days, "health_score": health, "commits": len(commits), "pull_requests": len(prs), "open_pull_requests": open_prs, "merged_pull_requests": merged_prs, "issues": len(issues), "open_issues": open_issues, "contributors": len({commit.author_login for commit in commits if commit.author_login}), "average_pr_size": average_pr_size}
