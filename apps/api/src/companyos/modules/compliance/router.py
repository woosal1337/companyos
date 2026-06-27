"""Compliance endpoints (COS-233)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from companyos.core.deps import OrgContext, OrgCtx, SessionDep, require_role
from companyos.core.schemas import SuccessResponse, ok
from companyos.modules.compliance import service
from companyos.modules.compliance.schemas import (
    CompliancePostureOut,
    DataSubjectExportOut,
    ErasureRequestIn,
    ErasureRequestOut,
)
from companyos.modules.orgs.models import OrgRole

router = APIRouter(prefix="/orgs/{org_id}/compliance", tags=["compliance"])

AdminCtx = Annotated[OrgContext, Depends(require_role(OrgRole.ADMIN))]


@router.get("")
async def get_posture(ctx: OrgCtx, session: SessionDep) -> SuccessResponse[CompliancePostureOut]:
    data = await service.posture(session, ctx)
    return ok(CompliancePostureOut.model_validate(data))


@router.get("/data-subjects/{user_id}/export")
async def data_subject_export(
    user_id: uuid.UUID, ctx: AdminCtx, session: SessionDep
) -> SuccessResponse[DataSubjectExportOut]:
    """Assemble a GDPR data-subject export bundle (admin) — COS-233."""
    data = await service.data_subject_export(session, ctx, user_id)
    return ok(DataSubjectExportOut.model_validate(data))


@router.post("/erasure-requests")
async def request_erasure(
    payload: ErasureRequestIn, ctx: AdminCtx, session: SessionDep
) -> SuccessResponse[ErasureRequestOut]:
    """File an audited right-to-erasure request (admin) — COS-233."""
    data = await service.request_erasure(session, ctx, payload.user_id, payload.reason)
    return ok(ErasureRequestOut.model_validate(data), message="Erasure request recorded")
