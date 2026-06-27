"""Ad-hoc analytics chart builder (COS-57)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_custom_chart_by_priority(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    for _ in range(2):
        await create_task(client, auth["headers"], org["id"], project["id"])

    chart = await client.get(
        f"{API}/orgs/{org['id']}/analytics/custom",
        params={"metric": "count", "dimension": "priority", "project_id": project["id"]},
        headers=auth["headers"],
    )
    assert chart.status_code == 200, chart.text
    data = chart.json()["data"]
    assert data["dimension"] == "priority"
    assert sum(point["value"] for point in data["points"]) == 2

    bad = await client.get(
        f"{API}/orgs/{org['id']}/analytics/custom",
        params={"dimension": "nope"},
        headers=auth["headers"],
    )
    assert bad.status_code == 404
