"""Unauthenticated public meeting-share endpoints (SAFE-01)."""

from fastapi import APIRouter

from companyos.core.deps import SessionDep
from companyos.core.schemas import SuccessResponse, ok
from companyos.modules.meetings import service
from companyos.modules.meetings.schemas import (
    PublicChatIn,
    PublicChatOut,
    PublicMeetingShareOut,
)

router = APIRouter(prefix="/share/meetings", tags=["public-share"])


@router.get("/{token}")
async def get_public_share(
    token: str, session: SessionDep
) -> SuccessResponse[PublicMeetingShareOut]:
    share = await service.get_public_share(session, token)
    return ok(share)


@router.post("/{token}/chat")
async def public_chat(
    token: str, payload: PublicChatIn, session: SessionDep
) -> SuccessResponse[PublicChatOut]:
    reply, grounded = await service.public_chat_about_meeting(session, token, payload)
    return ok(PublicChatOut(reply=reply, grounded=grounded))
