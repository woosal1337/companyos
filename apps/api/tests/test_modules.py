"""Module (workstream) CRUD + task linking tests (COS-27)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_modules_summary(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="MSU")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/modules"

    m1 = (await client.post(base, json={"name": "A"}, headers=auth["headers"])).json()["data"]
    await client.post(base, json={"name": "B"}, headers=auth["headers"])
    await client.post(
        base,
        json={"name": "Late", "target_date": "2020-01-01"},
        headers=auth["headers"],
    )
    await client.patch(f"{base}/{m1['id']}", json={"status": "completed"}, headers=auth["headers"])

    summary = await client.get(f"{base}/summary", headers=auth["headers"])
    assert summary.status_code == 200, summary.text
    data = summary.json()["data"]
    assert data["module_count"] == 3
    assert data["completed"] == 1
    assert data["delayed"] == 1


async def test_module_crud_and_rollup(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="MOD")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/modules"

    created = await client.post(
        base,
        json={"name": "Billing", "description": "Payments workstream", "target_date": "2026-08-15"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    module = created.json()["data"]
    assert module["name"] == "Billing"
    assert module["status"] == "planned"
    assert module["task_total"] == 0

    t1 = await create_task(client, auth["headers"], org["id"], project["id"], title="A")
    t2 = await create_task(client, auth["headers"], org["id"], project["id"], title="B")
    for task in (t1, t2):
        linked = await client.post(
            f"{base}/{module['id']}/tasks/{task['id']}", headers=auth["headers"]
        )
        assert linked.status_code == 201, linked.text
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{t1['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )

    listing = await client.get(base, headers=auth["headers"])
    row = listing.json()["data"][0]
    assert row["task_total"] == 2
    assert row["task_done"] == 1
    assert row["task_todo"] == 1

    fetched = await client.get(f"{API}/orgs/{org['id']}/tasks/{t1['id']}", headers=auth["headers"])
    assert fetched.json()["data"]["module_id"] == module["id"]

    unlinked = await client.delete(
        f"{base}/{module['id']}/tasks/{t2['id']}", headers=auth["headers"]
    )
    assert unlinked.status_code == 200
    updated = await client.patch(
        f"{base}/{module['id']}", json={"status": "in_progress"}, headers=auth["headers"]
    )
    assert updated.json()["data"]["status"] == "in_progress"
    assert updated.json()["data"]["task_total"] == 1

    deleted = await client.delete(f"{base}/{module['id']}", headers=auth["headers"])
    assert deleted.status_code == 200
    assert await client.get(base, headers=auth["headers"]) is not None
    assert (await client.get(base, headers=auth["headers"])).json()["data"] == []
