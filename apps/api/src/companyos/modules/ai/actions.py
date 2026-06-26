"""Build-mode AI actions: propose a structured change, confirm, then execute (COS-212).

The model only PROPOSES a structured action; nothing mutates until the caller
confirms via execute_action, and every execution runs through the normal
RBAC-checked service layer as the requesting user.
"""

import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from companyos.core.deps import OrgContext
from companyos.core.exceptions import BadRequestError, NotFoundError
from companyos.modules.ai.models import AIRunPurpose
from companyos.modules.ai.providers import ChatMessage
from companyos.modules.ai.service import run_completion
from companyos.modules.projects.models import Project
from companyos.modules.tasks.models import TaskPriority
from companyos.modules.tasks.schemas import TaskCreateIn

SUPPORTED_ACTIONS = ("create_task",)

_PROPOSE_SYSTEM = (
    "You convert a request into ONE structured workspace action. The only supported action "
    'is "create_task". Respond with ONLY compact JSON: '
    '{"action": "create_task", "project_key": "<KEY>", "title": "...", '
    '"description": "...", "priority": "none|low|medium|high|urgent"}. '
    "Choose project_key from the provided list. Keep the title concise."
)


async def propose_action(session: AsyncSession, ctx: OrgContext, prompt: str) -> dict[str, object]:
    """Ask the model for a structured action proposal (no mutation)."""
    projects = list(
        await session.scalars(
            select(Project).where(Project.org_id == ctx.org.id, Project.deleted_at.is_(None))
        )
    )
    if not projects:
        raise BadRequestError("Create a project before using Build mode")
    catalog = ", ".join(f"{p.key} ({p.name})" for p in projects[:50])
    messages: list[ChatMessage] = [
        {"role": "system", "content": _PROPOSE_SYSTEM},
        {"role": "user", "content": f"Projects: {catalog}\n\nRequest: {prompt.strip()}"},
    ]
    result, run = await run_completion(
        session, ctx, purpose=AIRunPurpose.CHAT, messages=messages, max_tokens=300
    )
    body = result.content.strip()
    start, end = body.find("{"), body.rfind("}")
    if start == -1 or end == -1:
        raise BadRequestError("The assistant could not produce a valid action")
    try:
        parsed = json.loads(body[start : end + 1])
    except ValueError as exc:
        raise BadRequestError("The assistant produced invalid action JSON") from exc

    action = str(parsed.get("action", ""))
    if action not in SUPPORTED_ACTIONS:
        raise BadRequestError(f"Unsupported action: {action or 'none'}")
    project_key = str(parsed.get("project_key", "")).strip()
    valid_keys = {p.key for p in projects}
    if project_key not in valid_keys:
        project_key = projects[0].key
    priority = str(parsed.get("priority", "none")).lower()
    if priority not in {p.value for p in TaskPriority}:
        priority = "none"
    title = str(parsed.get("title", "")).strip()[:500]
    if not title:
        raise BadRequestError("The proposed action has no title")
    return {
        "action": action,
        "params": {
            "project_key": project_key,
            "title": title,
            "description": str(parsed.get("description", "")).strip()[:4000] or None,
            "priority": priority,
        },
        "summary": f"Create work item “{title}” in {project_key} (priority: {priority})",
        "ai_run_id": run.id,
    }


async def execute_action(
    session: AsyncSession, ctx: OrgContext, action: str, params: dict[str, object]
) -> dict[str, object]:
    """Execute a previously-proposed action through the RBAC-checked service layer."""
    from companyos.modules.tasks.service import create_task  # noqa: PLC0415

    if action not in SUPPORTED_ACTIONS:
        raise BadRequestError(f"Unsupported action: {action}")
    project_key = str(params.get("project_key", "")).strip()
    project = await session.scalar(
        select(Project).where(
            Project.org_id == ctx.org.id, Project.key == project_key, Project.deleted_at.is_(None)
        )
    )
    if project is None:
        raise NotFoundError("Project not found")
    priority_raw = str(params.get("priority", "none")).lower()
    priority = (
        TaskPriority(priority_raw)
        if priority_raw in {p.value for p in TaskPriority}
        else TaskPriority.NONE
    )
    payload = TaskCreateIn(
        title=str(params.get("title", "")).strip()[:500] or "Untitled",
        description=(str(params["description"]) if params.get("description") else None),
        priority=priority,
    )
    task, created_project = await create_task(session, ctx, project.id, payload)
    identifier = f"{created_project.key}-{task.number}"
    return {"action": action, "task_id": task.id, "identifier": identifier, "title": task.title}
