"""Pivot/table chart analytics (COS-119)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_pivot_table(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    for _ in range(3):
        await create_task(client, auth["headers"], org["id"], project["id"])

    pivot = await client.get(
        f"{API}/orgs/{org['id']}/analytics/pivot",
        params={"row": "priority", "col": "status", "project_id": project["id"]},
        headers=auth["headers"],
    )
    assert pivot.status_code == 200, pivot.text
    data = pivot.json()["data"]
    assert data["row"] == "priority"
    assert data["col"] == "status"
    total = sum(sum(cols.values()) for cols in data["cells"].values())
    assert total == 3

    bad = await client.get(
        f"{API}/orgs/{org['id']}/analytics/pivot",
        params={"row": "nope", "col": "status"},
        headers=auth["headers"],
    )
    assert bad.status_code == 404
