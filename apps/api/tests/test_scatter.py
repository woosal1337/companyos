"""Cycle/module progress scatter analytics (COS-46)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_progress_scatter(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])

    cycle = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles",
        json={"name": "Sprint 1"},
        headers=auth["headers"],
    )
    assert cycle.status_code in (200, 201), cycle.text

    scatter = await client.get(
        f"{API}/orgs/{org['id']}/analytics/scatter",
        params={"dimension": "cycle", "project_id": project["id"]},
        headers=auth["headers"],
    )
    assert scatter.status_code == 200, scatter.text
    data = scatter.json()["data"]
    assert data["dimension"] == "cycle"
    assert isinstance(data["points"], list)

    bad = await client.get(
        f"{API}/orgs/{org['id']}/analytics/scatter",
        params={"dimension": "nope"},
        headers=auth["headers"],
    )
    assert bad.status_code == 404
