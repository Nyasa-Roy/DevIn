import base64
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import User
from app.security import encrypt_token

router = APIRouter(prefix="/auth", tags=["authentication"])
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


@router.get("/github")
def github_login(request: Request) -> RedirectResponse:
    settings = get_settings()
    if not settings.github_client_id:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="GitHub OAuth is not configured")
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    request.session["oauth_state"] = state
    request.session["oauth_verifier"] = verifier
    query = urlencode({"client_id": settings.github_client_id, "redirect_uri": settings.github_redirect_uri, "scope": settings.github_scope, "state": state, "code_challenge": challenge, "code_challenge_method": "S256"})
    return RedirectResponse(f"{GITHUB_AUTHORIZE_URL}?{query}")


@router.get("/github/callback")
async def github_callback(request: Request, code: str | None = None, state: str | None = None, db: Session = Depends(get_db)):
    settings = get_settings()
    verifier = request.session.pop("oauth_verifier", "")
    if not code or not state or not verifier or not secrets.compare_digest(state, request.session.pop("oauth_state", "")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OAuth callback state")
    if not settings.github_client_id or not settings.github_client_secret:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="GitHub OAuth is not configured")
    async with httpx.AsyncClient(timeout=10) as client:
        token_response = await client.post(GITHUB_TOKEN_URL, data={"client_id": settings.github_client_id, "client_secret": settings.github_client_secret, "code": code, "redirect_uri": settings.github_redirect_uri, "code_verifier": verifier}, headers={"Accept": "application/json"})
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="GitHub did not return an access token")
        user_response = await client.get(GITHUB_USER_URL, headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"})
        user_response.raise_for_status()
    github_user = user_response.json()
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=int(token_data["expires_in"])) if token_data.get("expires_in") else None
    refresh_token = token_data.get("refresh_token")
    user = db.scalar(select(User).where(User.github_id == github_user["id"]))
    if user is None:
        user = User(github_id=github_user["id"], login=github_user["login"], avatar_url=github_user.get("avatar_url"), github_token_encrypted=encrypt_token(access_token), github_refresh_token_encrypted=encrypt_token(refresh_token) if refresh_token else None, github_token_expires_at=expires_at)
        db.add(user)
    else:
        user.login = github_user["login"]
        user.avatar_url = github_user.get("avatar_url")
        user.github_token_encrypted = encrypt_token(access_token)
        user.github_refresh_token_encrypted = encrypt_token(refresh_token) if refresh_token else user.github_refresh_token_encrypted
        user.github_token_expires_at = expires_at
    db.commit()
    request.session["user_id"] = user.id
    request.session["csrf_token"] = secrets.token_urlsafe(32)
    return RedirectResponse(f"{settings.frontend_url}/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/me")
def current_user(request: Request, db: Session = Depends(get_db)) -> dict:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user = db.get(User, user_id)
    if user is None:
        request.session.clear()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return {"id": user.id, "github_id": user.github_id, "login": user.login, "avatar_url": user.avatar_url}


@router.get("/csrf")
def csrf_token(request: Request) -> dict[str, str]:
    token = request.session.get("csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        request.session["csrf_token"] = token
    return {"csrf_token": token}


def require_csrf(request: Request) -> None:
    expected = request.session.get("csrf_token")
    provided = request.headers.get("x-csrf-token")
    if not expected or not provided or not secrets.compare_digest(expected, provided):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing or invalid CSRF token")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, _: None = Depends(require_csrf)) -> None:
    request.session.clear()
