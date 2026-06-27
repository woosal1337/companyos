"""Per-member workload/capacity analytics (COS-75)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_member_workload(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    me_id = auth["user_id"]
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])

    task = await create_task(client, auth["headers"], org["id"], project["id"])
    await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}",
        json={"assignee_id": me_id},
        headers=auth["headers"],
    )

    workload = await client.get(
        f"{API}/orgs/{org['id']}/analytics/workload",
        params={"project_id": project["id"]},
        headers=auth["headers"],
    )
    assert workload.status_code == 200, workload.text
    members = workload.json()["data"]["members"]
    mine = next(m for m in members if m["assignee_id"] == me_id)
    assert mine["open"] >= 1
    assert "completed_30d" in mine
