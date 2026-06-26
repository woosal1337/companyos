"""Customizable dashboards + chart widgets (COS-94)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_dashboard_widget_flow(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    await create_task(client, h, org["id"], project["id"], title="One")
    await create_task(client, h, org["id"], project["id"], title="Two")
    base = f"{API}/orgs/{org['id']}/dashboards"

    created = await client.post(base, json={"name": "Ops"}, headers=h)
    assert created.status_code == 201, created.text
    did = created.json()["data"]["id"]

    listed = await client.get(base, headers=h)
    assert any(d["id"] == did for d in listed.json()["data"])

    widget = await client.post(
        f"{base}/{did}/widgets",
        json={
            "title": "By status",
            "config": {"chart_type": "bar", "metric": "count", "dimension": "status"},
        },
        headers=h,
    )
    assert widget.status_code == 201, widget.text
    wid = widget.json()["data"]["id"]
    assert widget.json()["data"]["config"]["dimension"] == "status"

    data = await client.get(f"{base}/{did}/data", headers=h)
    assert data.status_code == 200, data.text
    rows = data.json()["data"]
    assert len(rows) == 1
    assert rows[0]["widget_id"] == wid
    assert sum(p["value"] for p in rows[0]["points"]) == 2

    upd = await client.patch(
        f"{base}/{did}/widgets/{wid}",
        json={"config": {"chart_type": "donut", "metric": "count", "dimension": "priority"}},
        headers=h,
    )
    assert upd.json()["data"]["config"]["dimension"] == "priority"
    assert (await client.delete(f"{base}/{did}/widgets/{wid}", headers=h)).status_code == 200

    assert (await client.delete(f"{base}/{did}", headers=h)).status_code == 200
    assert (await client.get(f"{base}/{did}", headers=h)).status_code == 404
