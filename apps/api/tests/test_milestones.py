"""Milestone CRUD + work-item linking tests."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_milestone_bulk_link_and_list(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="MBL")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/milestones"
    milestone = (await client.post(base, json={"name": "Beta"}, headers=auth["headers"])).json()[
        "data"
    ]

    t1 = await create_task(client, auth["headers"], org["id"], project["id"], title="One")
    t2 = await create_task(client, auth["headers"], org["id"], project["id"], title="Two")

    bulk = await client.post(
        f"{base}/{milestone['id']}/tasks/bulk",
        json={"task_ids": [t1["id"], t2["id"], t1["id"]]},
        headers=auth["headers"],
    )
    assert bulk.status_code == 201, bulk.text
    statuses = [row["status"] for row in bulk.json()["data"]]
    assert statuses.count("linked") == 2
    assert statuses.count("skipped") == 1

    listing = await client.get(f"{base}/{milestone['id']}/tasks", headers=auth["headers"])
    assert listing.status_code == 200, listing.text
    assert {row["title"] for row in listing.json()["data"]} == {"One", "Two"}


async def test_milestone_lifecycle_and_progress(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="MLS")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/milestones"

    created = await client.post(
        base,
        json={"name": "Beta", "target_date": "2026-07-01", "description": "Public beta"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    milestone = created.json()["data"]
    assert milestone["status"] == "upcoming"
    assert milestone["task_total"] == 0

    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Ship")
    linked = await client.post(
        f"{base}/{milestone['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    assert linked.status_code == 201, linked.text

    fetched = await client.get(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    assert fetched.json()["data"]["milestone_id"] == milestone["id"]

    listing = await client.get(base, headers=auth["headers"])
    row = listing.json()["data"][0]
    assert row["task_total"] == 1
    assert row["task_done"] == 0

    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )
    listing2 = await client.get(base, headers=auth["headers"])
    assert listing2.json()["data"][0]["task_done"] == 1

    completed = await client.patch(
        f"{base}/{milestone['id']}", json={"status": "completed"}, headers=auth["headers"]
    )
    assert completed.json()["data"]["status"] == "completed"
