"""Initiative CRUD + project linking + rollup tests."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_initiative_updates(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    base = f"{API}/orgs/{org['id']}/initiatives"
    created = await client.post(base, json={"name": "Growth"}, headers=auth["headers"])
    initiative = created.json()["data"]
    updates = f"{base}/{initiative['id']}/updates"

    posted = await client.post(
        updates,
        json={"health": "off_track", "summary": "Two projects slipped."},
        headers=auth["headers"],
    )
    assert posted.status_code == 201, posted.text
    assert posted.json()["data"]["health"] == "off_track"

    listing = await client.get(updates, headers=auth["headers"])
    rows = listing.json()["data"]
    assert len(rows) == 1
    assert rows[0]["summary"] == "Two projects slipped."


async def test_initiative_lifecycle_and_rollup(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="INI")
    base = f"{API}/orgs/{org['id']}/initiatives"

    created = await client.post(
        base,
        json={"name": "Q3 Expansion", "target_date": "2026-09-30"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    initiative = created.json()["data"]
    assert initiative["status"] == "active"
    assert initiative["project_count"] == 0

    linked = await client.post(
        f"{base}/{initiative['id']}/projects/{project['id']}", headers=auth["headers"]
    )
    assert linked.status_code == 201, linked.text

    t1 = await create_task(client, auth["headers"], org["id"], project["id"], title="A")
    await create_task(client, auth["headers"], org["id"], project["id"], title="B")
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{t1['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )

    await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{t1['id']}",
        json={"estimate": "5"},
        headers=auth["headers"],
    )

    listing = await client.get(base, headers=auth["headers"])
    row = listing.json()["data"][0]
    assert row["project_count"] == 1
    assert row["task_total"] == 2
    assert row["task_done"] == 1
    assert row["task_todo"] == 1
    assert row["weighted_done"] == 5.0
    assert row["weighted_total"] == 6.0

    projects = await client.get(f"{base}/{initiative['id']}/projects", headers=auth["headers"])
    assert projects.json()["data"][0]["key"] == "INI"

    removed = await client.delete(
        f"{base}/{initiative['id']}/projects/{project['id']}", headers=auth["headers"]
    )
    assert removed.status_code == 200
    after = await client.get(base, headers=auth["headers"])
    assert after.json()["data"][0]["project_count"] == 0
