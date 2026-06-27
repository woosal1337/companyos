"""Board-card comment context on serialized tasks (AI-BE-01)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def _comment(
    client: AsyncClient, headers: dict[str, str], org_id: str, task_id: str, text: str
) -> None:
    response = await client.post(
        f"{API}/orgs/{org_id}/comments",
        json={"entity_type": "task", "entity_id": task_id, "content": text},
        headers=headers,
    )
    assert response.status_code == 201, response.text


async def test_task_exposes_comment_count_and_latest(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CMT")
    task = await create_task(client, auth["headers"], org["id"], project["id"])

    fresh = await client.get(f"{API}/orgs/{org['id']}/tasks/{task['id']}", headers=auth["headers"])
    assert fresh.json()["data"]["comment_count"] == 0
    assert fresh.json()["data"]["latest_comment"] is None

    await _comment(client, auth["headers"], org["id"], task["id"], "first comment")
    await _comment(client, auth["headers"], org["id"], task["id"], "waiting on design review")

    updated = await client.get(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    data = updated.json()["data"]
    assert data["comment_count"] == 2
    assert data["latest_comment"]["content"] == "waiting on design review"
    assert data["latest_comment"]["author_name"] == "Test User"
