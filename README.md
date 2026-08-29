# DevInsight

DevInsight is an AI-powered software engineering intelligence platform for GitHub repositories. It combines repository synchronisation, engineering analytics, pull-request risk prediction, anomaly detection, and semantic code search.

## Repository status

This repository is being implemented incrementally according to the SRS in `docs/project-plan.md`.

Current milestone: **Phase 0 + Phase 1 — project baseline and backend foundation**.

## Quick start

Requirements: Python 3.11+ and PostgreSQL (or SQLite for a lightweight local smoke test).

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The API is available at `http://localhost:8000`; interactive docs are at `/docs`.

Run tests from the backend directory with `pytest`.

## Planned structure

```text
frontend/       Next.js application (Phase 2+)
backend/        FastAPI application and persistence layer
ml/             Feature engineering and model pipeline (Phase 8+)
infrastructure/ Docker, CI/CD, and deployment assets (Phase 12+)
tests/          Cross-service test assets
docs/           Architecture, schema, API, and decision records
```

## Development principles

- Keep GitHub credentials and access tokens server-side.
- Keep synchronisation asynchronous once the queue is introduced.
- Make ML outputs explainable and treat risk as an assessment, never a guarantee.
- Prefer small, tested increments that preserve a runnable system.
