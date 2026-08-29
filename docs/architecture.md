# Architecture

DevInsight is a monorepo with a Next.js frontend, a FastAPI backend, PostgreSQL as the system of record, Redis/Celery for background work, and a Python ML pipeline.

The backend owns authentication, GitHub credentials, access boundaries, persistence, and orchestration. The frontend communicates with the backend over HTTP and never receives GitHub OAuth secrets.

The initial backend boundary is intentionally small:

```text
HTTP client -> FastAPI -> SQLAlchemy engine -> PostgreSQL
```

Later phases extend this with GitHub API ingestion, background jobs, analytics, and ML services without changing the public health/startup contract.
