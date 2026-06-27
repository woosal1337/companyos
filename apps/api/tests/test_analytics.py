"""Work-item analytics overview (COS-26)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_analytics_overview(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])

    a = await create_task(client, auth["headers"], org["id"], project["id"], title="A")
    await create_task(client, auth["headers"], org["id"], project["id"], title="B")
    bug = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Bug", kind="bug", severity="high"
    )
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{a['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )

    overview = await client.get(
        f"{API}/orgs/{org['id']}/analytics/overview", headers=auth["headers"]
    )
    assert overview.status_code == 200, overview.text
    data = overview.json()["data"]
    assert data["total"] == 3
    assert data["completed"] == 1
    assert round(data["completion_rate"], 4) == round(1 / 3, 4)
    assert data["by_category"]["completed"] == 1
    assert data["by_category"]["backlog"] == 2
    assert data["by_kind"]["bug"] == 1
    assert data["by_kind"]["task"] == 2

    scoped = await client.get(
        f"{API}/orgs/{org['id']}/analytics/overview?project_id={project['id']}",
        headers=auth["headers"],
    )
    assert scoped.json()["data"]["total"] == 3

    bad = await client.get(
        f"{API}/orgs/{org['id']}/analytics/overview?project_id=00000000-0000-0000-0000-000000000000",
        headers=auth["headers"],
    )
    assert bad.status_code == 404
    assert bug["id"]


async def test_analytics_csv_export(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    await create_task(client, auth["headers"], org["id"], project["id"], title="A")

    export = await client.get(
        f"{API}/orgs/{org['id']}/analytics/export.csv", headers=auth["headers"]
    )
    assert export.status_code == 200
    assert export.headers["content-type"].startswith("text/csv")
    body = export.text
    assert "metric,dimension,value" in body
    assert "total,,1" in body
    assert "by_category,backlog,1" in body


async def test_flow_analytics(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])

    backlog = await create_task(client, auth["headers"], org["id"], project["id"], title="B")
    started = await create_task(client, auth["headers"], org["id"], project["id"], title="S")
    await create_task(client, auth["headers"], org["id"], project["id"], title="B2")
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{started['id']}/status",
        json={"status": "in_progress"},
        headers=auth["headers"],
    )

    flow = await client.get(f"{API}/orgs/{org['id']}/analytics/flow", headers=auth["headers"])
    assert flow.status_code == 200, flow.text
    data = flow.json()["data"]
    assert data["total_wip"] == 3
    wip_by_status = {s["status"]: s["wip"] for s in data["statuses"]}
    assert wip_by_status["backlog"] == 2
    assert wip_by_status["started"] == 1
    assert [s["status"] for s in data["statuses"]].index("backlog") < [
        s["status"] for s in data["statuses"]
    ].index("started")
    assert backlog["id"]
