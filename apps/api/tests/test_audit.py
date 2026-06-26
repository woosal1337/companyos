"""Compliance audit-log tests (COS-241)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    create_task,
    register_and_login,
)


async def test_audit_log_filter_and_export(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="AUD")
    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Audited")
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "in_progress"},
        headers=auth["headers"],
    )

    audit = await client.get(f"{API}/orgs/{org['id']}/audit", headers=auth["headers"])
    assert audit.status_code == 200, audit.text
    items = audit.json()["data"]["items"]
    assert len(items) > 0
    entry = items[0]
    assert entry["actor_type"] == "user"
    assert entry["actor_name"]

    filtered = await client.get(
        f"{API}/orgs/{org['id']}/audit?entity_type=task", headers=auth["headers"]
    )
    assert all(item["entity_type"] == "task" for item in filtered.json()["data"]["items"])

    export = await client.get(f"{API}/orgs/{org['id']}/audit/export.csv", headers=auth["headers"])
    assert export.status_code == 200, export.text
    assert export.headers["content-type"].startswith("text/csv")
    body = export.text
    assert "timestamp,actor,actor_type" in body
    assert "task" in body


async def test_audit_log_requires_admin(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member)

    response = await client.get(f"{API}/orgs/{org['id']}/audit", headers=member["headers"])
    assert response.status_code == 403
