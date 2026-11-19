from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.db import Base
from app.models import PullRequest, Repository
from app.tasks import _persist_snapshot


def test_persist_snapshot_stores_pull_request_review_features() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        repository = Repository(github_id=10, owner_id=1, name="api", full_name="team/api", html_url="https://github.com/team/api")
        db.add(repository)
        db.flush()
        _persist_snapshot(db, repository.id, {"pull_requests": [{"number": 7, "title": "Safer sync", "state": "open", "changed_files": 4, "additions": 120, "deletions": 30, "review_count": 1, "user": {"login": "alice"}}]})
        db.commit()
        pull_request = db.scalar(select(PullRequest).where(PullRequest.repository_id == repository.id))

    assert pull_request is not None
    assert pull_request.github_number == 7
    assert pull_request.changed_files == 4
    assert pull_request.additions == 120
    assert pull_request.deletions == 30
    assert pull_request.reviews == 1
