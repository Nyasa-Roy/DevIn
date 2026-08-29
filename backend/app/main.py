from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text

from app.config import get_settings
from app.db import engine
from app.db import Base
from app.api.auth import router as auth_router
from app.api.repositories import router as repositories_router
from app.api.pull_requests import router as pull_requests_router
from app.api.intelligence import router as intelligence_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    yield
    engine.dispose()


app = FastAPI(title=get_settings().app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=get_settings().secret_key, https_only=get_settings().environment == "production", same_site="lax")
app.include_router(auth_router)
app.include_router(repositories_router)
app.include_router(pull_requests_router)
app.include_router(intelligence_router)


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    return {"name": "DevInsight API", "status": "ok"}


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}
