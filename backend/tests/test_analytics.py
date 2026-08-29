from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db import Base
from app.models import Commit, Issue, PullRequest, Repository
from app.services.analytics import repository_metrics


def test_repository_metrics_aggregate_activity() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        repository = Repository(github_id=10, owner_id=1, name="api", full_name="team/api", html_url="https://github.com/team/api")
        db.add(repository)
        db.flush()
        db.add_all([
            Commit(repository_id=repository.id, sha="a" * 40, author_login="alice", message="Add endpoint", committed_at=datetime.now(timezone.utc)),
            Commit(repository_id=repository.id, sha="b" * 40, author_login="bob", message="Fix endpoint", committed_at=datetime.now(timezone.utc)),
            PullRequest(repository_id=repository.id, github_number=1, title="Feature", state="open", additions=20, deletions=5),
            Issue(repository_id=repository.id, github_number=2, title="Bug", state="open"),
        ])
        db.commit()
        metrics = repository_metrics(db, repository)
    assert metrics["commits"] == 2
    assert metrics["contributors"] == 2
    assert metrics["open_pull_requests"] == 1
    assert metrics["open_issues"] == 1
    assert metrics["average_pr_size"] == 25
