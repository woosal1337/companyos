"""Tenancy isolation: cross-org access must yield 404/403, never data."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    create_org,
    create_project,
    create_task,
    import_meeting,
    register_and_login,
)


async def test_cross_org_reads_return_404(client: AsyncClient) -> None:
    user_a = await register_and_login(client)
    user_b = await register_and_login(client)
    org_a = await create_org(client, user_a["headers"], name="Org A")
    await create_org(client, user_b["headers"], name="Org B")
    project_a = await create_project(client, user_a["headers"], org_a["id"], key="ALFA")
    task_a = await create_task(client, user_a["headers"], org_a["id"], project_a["id"])
    meeting_a = await import_meeting(client, user_a["headers"], org_a["id"])

    assert (
        await client.get(f"{API}/orgs/{org_a['id']}", headers=user_b["headers"])
    ).status_code == 404
    assert (
        await client.get(f"{API}/orgs/{org_a['id']}/projects", headers=user_b["headers"])
    ).status_code == 404
    assert (
        await client.get(
            f"{API}/orgs/{org_a['id']}/tasks/{task_a['id']}", headers=user_b["headers"]
        )
    ).status_code == 404
    assert (
        await client.get(
            f"{API}/orgs/{org_a['id']}/meetings/{meeting_a['id']}", headers=user_b["headers"]
        )
    ).status_code == 404
    assert (
        await client.get(f"{API}/orgs/{org_a['id']}/activity", headers=user_b["headers"])
    ).status_code == 404


async def test_cross_org_writes_return_404(client: AsyncClient) -> None:
    user_a = await register_and_login(client)
    user_b = await register_and_login(client)
    org_a = await create_org(client, user_a["headers"], name="Org A")
    org_b = await create_org(client, user_b["headers"], name="Org B")
    project_a = await create_project(client, user_a["headers"], org_a["id"], key="ALFA")
    task_a = await create_task(client, user_a["headers"], org_a["id"], project_a["id"])

    update = await client.patch(
        f"{API}/orgs/{org_a['id']}", json={"name": "Stolen"}, headers=user_b["headers"]
    )
    assert update.status_code == 404
    create = await client.post(
        f"{API}/orgs/{org_a['id']}/projects/{project_a['id']}/tasks",
        json={"title": "Injected"},
        headers=user_b["headers"],
    )
    assert create.status_code == 404
    comment = await client.post(
        f"{API}/orgs/{org_b['id']}/comments",
        json={"entity_type": "task", "entity_id": task_a["id"], "content": "leak?"},
        headers=user_b["headers"],
    )
    assert comment.status_code == 404


async def test_task_in_foreign_project_unreachable(client: AsyncClient) -> None:
    user_a = await register_and_login(client)
    user_b = await register_and_login(client)
    org_a = await create_org(client, user_a["headers"], name="Org A")
    org_b = await create_org(client, user_b["headers"], name="Org B")
    project_a = await create_project(client, user_a["headers"], org_a["id"], key="ALFA")
    task_a = await create_task(client, user_a["headers"], org_a["id"], project_a["id"])

    via_own_org = await client.get(
        f"{API}/orgs/{org_b['id']}/tasks/{task_a['id']}", headers=user_b["headers"]
    )
    assert via_own_org.status_code == 404
