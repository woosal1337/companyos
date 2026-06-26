"""Saved task view read/write tools."""

import uuid
from typing import Any

from mcp.types import ToolAnnotations

from companyos.modules.mcp_server.idempotency import run_idempotent
from companyos.modules.mcp_server.instance import mcp
from companyos.modules.mcp_server.principal import mcp_call
from companyos.modules.views import service as views_service
from companyos.modules.views.schemas import TaskViewIn, TaskViewUpdateIn


@mcp.tool
async def list_views() -> dict[str, Any]:
    """List the caller's personal views plus all team views."""
    async with mcp_call("views:read") as call:
        views = await views_service.list_views(call.session, call.ctx)
        items = [views_service.view_to_out(view).model_dump(mode="json") for view in views]
        return {"total": len(items), "items": items}


@mcp.tool
async def create_view(
    name: str,
    config: dict[str, Any] | None = None,
    scope: str = "personal",
    team_id: str | None = None,
    is_default: bool = False,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Save a named view (scope: personal, team, or teamspace; teamspace needs team_id)."""
    async with mcp_call("views:write") as call:

        async def _produce() -> dict[str, Any]:
            payload = TaskViewIn(
                name=name,
                config=config or {},
                scope=scope,
                team_id=uuid.UUID(team_id) if team_id else None,
                is_default=is_default,
            )
            view = await views_service.create_view(call.session, call.ctx, payload)
            return views_service.view_to_out(view).model_dump(mode="json")

        return await run_idempotent(
            call.session,
            org_id=call.ctx.org.id,
            key=idempotency_key,
            tool="create_view",
            producer=_produce,
        )


@mcp.tool
async def update_view(
    view_id: str,
    name: str | None = None,
    config: dict[str, Any] | None = None,
    is_default: bool | None = None,
) -> dict[str, Any]:
    """Update a view's name, config, or default flag."""
    async with mcp_call("views:write") as call:
        payload = TaskViewUpdateIn(name=name, config=config, is_default=is_default)
        view = await views_service.update_view(call.session, call.ctx, uuid.UUID(view_id), payload)
        return views_service.view_to_out(view).model_dump(mode="json")


@mcp.tool(annotations=ToolAnnotations(destructiveHint=True, idempotentHint=True))
async def delete_view(view_id: str, confirm: bool = False) -> dict[str, Any]:
    """Delete a saved view. Call with confirm=false to preview, then confirm=true to delete."""
    async with mcp_call("views:write") as call:
        target = next(
            (
                view
                for view in await views_service.list_views(call.session, call.ctx)
                if str(view.id) == view_id
            ),
            None,
        )
        if target is None:
            return {"deleted": False, "view_id": view_id, "error": "View not found"}
        if not confirm:
            return {
                "requires_confirmation": True,
                "action": "delete_view",
                "view_id": view_id,
                "name": target.name,
                "hint": "Re-call delete_view with confirm=true to permanently delete.",
            }
        await views_service.delete_view(call.session, call.ctx, uuid.UUID(view_id))
        return {"deleted": True, "view_id": view_id}
