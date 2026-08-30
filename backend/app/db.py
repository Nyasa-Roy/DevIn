from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def _engine_kwargs(database_url: str) -> dict:
    return {"connect_args": {"check_same_thread": False}} if database_url.startswith("sqlite") else {}


engine = create_engine(
    get_settings().database_url,
    future=True,
    pool_pre_ping=True,
    **_engine_kwargs(get_settings().database_url),
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def apply_local_schema_updates() -> None:
    """Add columns introduced after the initial SQLite development database."""
    if not get_settings().database_url.startswith("sqlite"):
        return
    additions = {"users": {"github_token_encrypted": "VARCHAR(4096)"}, "pull_requests": {"reviews": "INTEGER NOT NULL DEFAULT 0"}}
    inspector = inspect(engine)
    with engine.begin() as connection:
        for table, columns in additions.items():
            if table not in inspector.get_table_names():
                continue
            existing = {column["name"] for column in inspector.get_columns(table)}
            for name, definition in columns.items():
                if name not in existing:
                    connection.execute(text(f'ALTER TABLE "{table}" ADD COLUMN "{name}" {definition}'))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
