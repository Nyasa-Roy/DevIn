# API reference

Interactive OpenAPI documentation is available at `/docs` when the backend is running.

System: `GET /`, `GET /health`.

Authentication: `GET /auth/github`, `GET /auth/github/callback`, `GET /auth/me`, `POST /auth/logout`.

Repositories: `GET /repositories`, `POST /repositories/{github_id}/connect`, `DELETE /repositories/{id}`, `POST /repositories/{id}/sync`, `GET /repositories/{id}/sync/{job_id}`.

Analytics: `GET /repositories/{id}/overview`, `GET /repositories/{id}/metrics`, `GET /repositories/{id}/activity`.

Intelligence: `GET /repositories/{id}/pull-requests`, `GET /pull-requests/{id}/risk`, `GET /repositories/{id}/anomalies`, `POST /repositories/{id}/search`.
