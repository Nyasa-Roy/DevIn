from fastapi.testclient import TestClient

from app.main import app


def test_root() -> None:
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}


def test_github_login_requires_configuration() -> None:
    with TestClient(app) as client:
        response = client.get("/auth/github")
    assert response.status_code == 503
    assert response.json()["detail"] == "GitHub OAuth is not configured"


def test_current_user_requires_session() -> None:
    with TestClient(app) as client:
        response = client.get("/auth/me")
    assert response.status_code == 401


def test_repositories_requires_session() -> None:
    with TestClient(app) as client:
        response = client.get("/repositories")
    assert response.status_code == 401


def test_pull_request_risk_requires_session() -> None:
    with TestClient(app) as client:
        response = client.get("/pull-requests/1/risk")
    assert response.status_code == 401
