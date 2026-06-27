"""Auth-provider endpoints (COS-209)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response

from companyos.core.config import get_settings
from companyos.core.deps import OrgContext, OrgCtx, SessionDep, require_role
from companyos.core.schemas import SuccessResponse, ok
from companyos.core.security import create_access_token, create_refresh_token
from companyos.modules.auth.schemas import UserOut
from companyos.modules.auth_providers import service
from companyos.modules.auth_providers.schemas import (
    AuthProviderConfigIn,
    AuthProviderConfigOut,
    PublicProvidersOut,
)
from companyos.modules.orgs.models import OrgRole

admin_router = APIRouter(prefix="/orgs/{org_id}/auth-providers", tags=["auth-providers"])
public_router = APIRouter(prefix="/auth", tags=["auth-providers"])

AdminCtx = Annotated[OrgContext, Depends(require_role(OrgRole.ADMIN))]


def _set_auth_cookies(response: Response, access: str, refresh: str) -> None:
    settings = get_settings()
    secure = settings.env == "production"
    response.set_cookie(
        "access_token",
        access,
        max_age=settings.access_token_expire_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=settings.refresh_token_expire_days * 86400,
        httponly=True,
        samesite="lax",
        secure=secure,
    )


@admin_router.get("")
async def get_config(ctx: OrgCtx, session: SessionDep) -> SuccessResponse[AuthProviderConfigOut]:
    config = await service.get_config(session, ctx)
    return ok(AuthProviderConfigOut.model_validate(config))


@admin_router.put("")
async def update_config(
    payload: AuthProviderConfigIn, ctx: AdminCtx, session: SessionDep
) -> SuccessResponse[AuthProviderConfigOut]:
    config = await service.update_config(session, ctx, **payload.model_dump(exclude_unset=True))
    return ok(AuthProviderConfigOut.model_validate(config), message="Sign-in providers updated")


@public_router.get("/providers")
async def public_providers() -> SuccessResponse[PublicProvidersOut]:
    """Which sign-in methods the login screen should offer (COS-209)."""
    configured = service.configured_providers()
    return ok(PublicProvidersOut(google=configured["google"], github=configured["github"]))


@public_router.get("/oauth/{provider}/start")
async def oauth_start(provider: str) -> SuccessResponse[dict[str, str]]:
    """Begin a Google/GitHub sign-in: returns the authorization URL (COS-209)."""
    return ok({"authorization_url": service.authorization_url(provider)})


@public_router.get("/oauth/{provider}/callback")
async def oauth_callback(
    provider: str,
    response: Response,
    session: SessionDep,
    code: Annotated[str, Query()],
    state: Annotated[str, Query()],
) -> SuccessResponse[UserOut]:
    """Complete a social sign-in, JIT-provisioning the user + a session (COS-209)."""
    user = await service.complete_login(session, provider, code, state)
    _set_auth_cookies(response, create_access_token(user.id), create_refresh_token(user.id))
    return ok(UserOut.model_validate(user), message="Signed in")
