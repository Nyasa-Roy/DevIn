import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import File


def search_files(db: Session, repository_id: int, query: str, limit: int = 10) -> list[dict]:
    terms = {term for term in re.findall(r"[a-z0-9_]+", query.lower()) if len(term) > 1}
    results = []
    for file in db.scalars(select(File).where(File.repository_id == repository_id)).all():
        haystack = f"{file.path} {file.content}".lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            results.append({"path": file.path, "score": score, "snippet": file.content[:240]})
    return sorted(results, key=lambda item: item["score"], reverse=True)[:limit]
