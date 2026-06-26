"""Auth-provider config + Google/GitHub OAuth login (COS-209)."""

import secrets
from typing import Any
from urllib.parse import urlencode

import httpx
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from companyos.core.config import get_settings
from companyos.core.deps import OrgContext
from companyos.core.exceptions import BadRequestError, UnauthorizedError
from companyos.core.security import hash_password
from companyos.modules.auth_providers.models import AuthProviderConfig
from companyos.modules.users.models import User

_STATE_TTL = 600

_ENDPOINTS = {
    "google": {
        "authorize": "https://accounts.google.com/o/oauth2/v2/auth",
        "token": "https://oauth2.googleapis.com/token",
        "userinfo": "https://www.googleapis.com/oauth2/v3/userinfo",
        "scope": "openid email profile",
    },
    "github": {
        "authorize": "https://github.com/login/oauth/authorize",
        "token": "https://github.com/login/oauth/access_token",
        "userinfo": "https://api.github.com/user",
        "scope": "read:user user:email",
    },
}


def _creds(provider: str) -> tuple[str, str, str]:
    s = get_settings()
    if provider == "google":
        return s.google_client_id, s.google_client_secret, s.google_redirect_uri
    if provider == "github":
        return s.github_client_id, s.github_client_secret, s.github_redirect_uri
    raise BadRequestError("Unknown provider")


def configured_providers() -> dict[str, bool]:
    """Which OAuth providers have instance credentials configured (COS-209)."""
    s = get_settings()
    return {
        "google": bool(s.google_client_id and s.google_client_secret),
        "github": bool(s.github_client_id and s.github_client_secret),
    }


async def get_config(session: AsyncSession, ctx: OrgContext) -> AuthProviderConfig:
    config = await session.scalar(
        select(AuthProviderConfig).where(AuthProviderConfig.org_id == ctx.org.id)
    )
    if config is None:
        config = AuthProviderConfig(org_id=ctx.org.id)
        session.add(config)
        await session.flush()
    return config


async def update_config(
    session: AsyncSession, ctx: OrgContext, **fields: bool | None
) -> AuthProviderConfig:
    config = await get_config(session, ctx)
    for key, value in fields.items():
        if value is not None and hasattr(config, key):
            setattr(config, key, value)
    await session.flush()
    return config


async def exchange_code(provider: str, code: str) -> str:
    client_id, client_secret, redirect_uri = _creds(provider)
    ep = _ENDPOINTS[provider]
    async with httpx.AsyncClient(timeout=8.0) as http:
        resp = await http.post(
            ep["token"],
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
        )
        resp.raise_for_status()
        return str(resp.json()["access_token"])


async def fetch_identity(provider: str, access_token: str) -> tuple[str, str]:
    """Return (email, name) from the provider's userinfo (COS-209)."""
    ep = _ENDPOINTS[provider]
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    async with httpx.AsyncClient(timeout=8.0) as http:
        resp = await http.get(ep["userinfo"], headers=headers)
        resp.raise_for_status()
        info: dict[str, Any] = dict(resp.json())
        email = str(info.get("email") or "")
        name = str(info.get("name") or info.get("login") or "")
        if not email and provider == "github":
            emails = await http.get("https://api.github.com/user/emails", headers=headers)
            if emails.status_code < 400:
                primary = next(
                    (e for e in emails.json() if e.get("primary") and e.get("verified")), None
                )
                if primary:
                    email = str(primary["email"])
    return email.strip().lower(), name


def _sign_state(provider: str) -> str:
    import time  # noqa: PLC0415

    payload = {"p": provider, "exp": int(time.time()) + _STATE_TTL}
    return jwt.encode(payload, get_settings().jwt_secret_key, algorithm="HS256")


def _verify_state(state: str, provider: str) -> None:
    try:
        payload = jwt.decode(state, get_settings().jwt_secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError("Invalid or expired OAuth state") from exc
    if payload.get("p") != provider:
        raise UnauthorizedError("OAuth state/provider mismatch")


def authorization_url(provider: str) -> str:
    if provider not in _ENDPOINTS:
        raise BadRequestError("Unknown provider")
    client_id, _secret, redirect_uri = _creds(provider)
    if not client_id:
        raise BadRequestError(f"{provider} sign-in is not configured")
    ep = _ENDPOINTS[provider]
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": ep["scope"],
        "state": _sign_state(provider),
    }
    return f"{ep['authorize']}?{urlencode(params)}"


async def complete_login(session: AsyncSession, provider: str, code: str, state: str) -> User:
    _verify_state(state, provider)
    token = await exchange_code(provider, code)
    email, name = await fetch_identity(provider, token)
    if not email:
        raise UnauthorizedError("The provider did not return a verified email")
    user = await session.scalar(select(User).where(User.email == email))
    if user is None:
        user = User(
            email=email,
            password_hash=hash_password(secrets.token_urlsafe(32)),
            full_name=name or email.split("@")[0],
            email_verified=True,
        )
        session.add(user)
        await session.flush()
    return user
