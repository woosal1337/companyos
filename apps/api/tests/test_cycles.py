"""Cycle CRUD + task assignment tests."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_cycle_crud_and_assignment(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CYC")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles"

    created = await client.post(
        base,
        json={"name": "Sprint 1", "start_date": "2026-06-01", "end_date": "2026-06-14"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    cycle = created.json()["data"]
    assert cycle["name"] == "Sprint 1"
    assert cycle["task_total"] == 0

    task = await create_task(client, auth["headers"], org["id"], project["id"])
    assigned = await client.post(
        f"{base}/{cycle['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    assert assigned.status_code == 201, assigned.text

    listing = await client.get(base, headers=auth["headers"])
    rows = listing.json()["data"]
    assert rows[0]["task_total"] == 1

    removed = await client.delete(
        f"{base}/{cycle['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    assert removed.status_code == 200
    listing2 = await client.get(base, headers=auth["headers"])
    assert listing2.json()["data"][0]["task_total"] == 0


async def test_active_cycles_workspace_dashboard(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    p1 = await create_project(client, auth["headers"], org["id"], key="ACA")
    p2 = await create_project(client, auth["headers"], org["id"], key="ACB")

    async def make_active(project_id: str, name: str) -> None:
        base = f"{API}/orgs/{org['id']}/projects/{project_id}/cycles"
        cycle = (await client.post(base, json={"name": name}, headers=auth["headers"])).json()[
            "data"
        ]
        await client.post(f"{base}/{cycle['id']}/start", headers=auth["headers"])

    await make_active(p1["id"], "P1 Sprint")
    await make_active(p2["id"], "P2 Sprint")
    await client.post(
        f"{API}/orgs/{org['id']}/projects/{p1['id']}/cycles",
        json={"name": "Future"},
        headers=auth["headers"],
    )

    active = await client.get(f"{API}/orgs/{org['id']}/cycles/active", headers=auth["headers"])
    assert active.status_code == 200, active.text
    rows = active.json()["data"]
    assert len(rows) == 2
    names = {row["name"] for row in rows}
    assert names == {"P1 Sprint", "P2 Sprint"}
    assert {row["project_key"] for row in rows} == {"ACA", "ACB"}


async def test_cycle_start_and_complete(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CYL")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles"

    created = await client.post(base, json={"name": "Sprint 1"}, headers=auth["headers"])
    cycle = created.json()["data"]
    assert cycle["status"] == "upcoming"

    started = await client.post(f"{base}/{cycle['id']}/start", headers=auth["headers"])
    assert started.status_code == 200, started.text
    started_data = started.json()["data"]
    assert started_data["status"] == "active"
    assert started_data["started_at"] is not None

    completed = await client.post(f"{base}/{cycle['id']}/complete", headers=auth["headers"])
    assert completed.status_code == 200, completed.text
    completed_data = completed.json()["data"]
    assert completed_data["status"] == "completed"
    assert completed_data["completed_at"] is not None


async def test_completed_cycle_is_locked(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="LCK")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles"
    cycle = (await client.post(base, json={"name": "S1"}, headers=auth["headers"])).json()["data"]

    done = await create_task(client, auth["headers"], org["id"], project["id"], title="done")
    await client.post(f"{base}/{cycle['id']}/tasks/{done['id']}", headers=auth["headers"])
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{done['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )
    open_task = await create_task(client, auth["headers"], org["id"], project["id"], title="open")
    await client.post(f"{base}/{cycle['id']}/tasks/{open_task['id']}", headers=auth["headers"])

    completed = await client.post(f"{base}/{cycle['id']}/complete", headers=auth["headers"])
    frozen = completed.json()["data"]
    assert frozen["final_total_count"] == 2
    assert frozen["final_completed_count"] == 1

    edit = await client.patch(
        f"{base}/{cycle['id']}", json={"name": "renamed"}, headers=auth["headers"]
    )
    assert edit.status_code == 400
    another = await create_task(client, auth["headers"], org["id"], project["id"], title="late")
    add = await client.post(f"{base}/{cycle['id']}/tasks/{another['id']}", headers=auth["headers"])
    assert add.status_code == 400
    remove = await client.delete(
        f"{base}/{cycle['id']}/tasks/{open_task['id']}", headers=auth["headers"]
    )
    assert remove.status_code == 400

    restart = await client.post(f"{base}/{cycle['id']}/start", headers=auth["headers"])
    assert restart.status_code == 400


async def test_cycle_velocity(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="VEL")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles"

    for done_count, total in ((2, 2), (1, 3)):
        cycle = (
            await client.post(base, json={"name": f"S{total}"}, headers=auth["headers"])
        ).json()["data"]
        for i in range(total):
            task = await create_task(
                client, auth["headers"], org["id"], project["id"], title=f"{total}-{i}"
            )
            await client.post(f"{base}/{cycle['id']}/tasks/{task['id']}", headers=auth["headers"])
            if i < done_count:
                await client.post(
                    f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
                    json={"status": "done"},
                    headers=auth["headers"],
                )
        await client.post(f"{base}/{cycle['id']}/complete", headers=auth["headers"])

    velocity = await client.get(f"{base}/velocity", headers=auth["headers"])
    assert velocity.status_code == 200, velocity.text
    data = velocity.json()["data"]
    assert data["cycle_count"] == 2
    assert [c["completed"] for c in data["cycles"]] == [2, 1]
    assert data["average_velocity"] == 1.5


async def test_cycle_transfer_incomplete(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="TRN")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles"
    source = (await client.post(base, json={"name": "S1"}, headers=auth["headers"])).json()["data"]
    target = (await client.post(base, json={"name": "S2"}, headers=auth["headers"])).json()["data"]

    open_task = await create_task(client, auth["headers"], org["id"], project["id"], title="Open")
    done_task = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Done", status="done"
    )
    for task in (open_task, done_task):
        assigned = await client.post(
            f"{base}/{source['id']}/tasks/{task['id']}", headers=auth["headers"]
        )
        assert assigned.status_code == 201, assigned.text

    transferred = await client.post(
        f"{base}/{source['id']}/transfer",
        json={"target_cycle_id": target["id"]},
        headers=auth["headers"],
    )
    assert transferred.status_code == 200, transferred.text
    assert transferred.json()["data"]["moved"] == 1

    rows = {
        row["id"]: row for row in (await client.get(base, headers=auth["headers"])).json()["data"]
    }
    assert rows[target["id"]]["task_total"] == 1
    assert rows[source["id"]]["task_total"] == 1


async def test_cycle_invalid_dates_rejected(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CYD")
    response = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles",
        json={"name": "Bad", "start_date": "2026-06-14", "end_date": "2026-06-01"},
        headers=auth["headers"],
    )
    assert response.status_code == 400
