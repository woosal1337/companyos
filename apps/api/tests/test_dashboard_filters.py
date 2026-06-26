"""Three-level PQL-driven dashboard filter layering (COS-104)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def _count_by_key(points: list[dict], key: str) -> int:
    return next((p["value"] for p in points if p["key"] == key), 0)


async def test_three_level_pql_filter(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="DSH")
    for title, pr in [("a", "high"), ("b", "high"), ("c", "low"), ("d", "low")]:
        t = await create_task(client, h, org["id"], project["id"], title=title)
        await client.patch(
            f"{API}/orgs/{org['id']}/tasks/{t['id']}", json={"priority": pr}, headers=h
        )
    base = f"{API}/orgs/{org['id']}/dashboards"

    dash = await client.post(base, json={"name": "Ops", "filter": "priority = high"}, headers=h)
    assert dash.status_code == 201, dash.text
    assert dash.json()["data"]["filter"] == "priority = high"
    did = dash.json()["data"]["id"]

    await client.post(
        f"{base}/{did}/widgets",
        json={
            "title": "By status",
            "config": {"chart_type": "bar", "metric": "count", "dimension": "status"},
        },
        headers=h,
    )
    data = await client.get(f"{base}/{did}/data", headers=h)
    assert data.status_code == 200, data.text
    pts = data.json()["data"][0]["points"]
    assert sum(p["value"] for p in pts) == 2

    data2 = await client.get(f"{base}/{did}/data", params={"q": "priority = low"}, headers=h)
    assert sum(p["value"] for p in data2.json()["data"][0]["points"]) == 0

    await client.post(
        f"{base}/{did}/widgets",
        json={
            "title": "Done only",
            "config": {"dimension": "priority", "metric": "count", "filter": "status = done"},
        },
        headers=h,
    )
    data3 = await client.get(f"{base}/{did}/data", headers=h)
    done_widget = data3.json()["data"][1]
    assert sum(p["value"] for p in done_widget["points"]) == 0
