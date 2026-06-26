"""Portfolio project states: seed, CRUD, assign, group (COS-240)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_project_states_seed_assign_and_group(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    base = f"{API}/orgs/{org['id']}/project-states"

    seeded = await client.get(base, headers=auth["headers"])
    assert seeded.status_code == 200, seeded.text
    states = seeded.json()["data"]
    assert [s["group"] for s in states] == [
        "draft",
        "planning",
        "execution",
        "monitoring",
        "completed",
        "cancelled",
    ]
    again = await client.get(base, headers=auth["headers"])
    assert len(again.json()["data"]) == 6

    execution = next(s for s in states if s["group"] == "execution")

    project = await create_project(client, auth["headers"], org["id"])
    updated = await client.patch(
        f"{API}/orgs/{org['id']}/projects/{project['id']}",
        json={"state_id": execution["id"]},
        headers=auth["headers"],
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["data"]["state_id"] == execution["id"]

    bad = await client.patch(
        f"{API}/orgs/{org['id']}/projects/{project['id']}",
        json={"state_id": "00000000-0000-0000-0000-000000000000"},
        headers=auth["headers"],
    )
    assert bad.status_code == 400

    cleared = await client.patch(
        f"{API}/orgs/{org['id']}/projects/{project['id']}",
        json={"clear_state": True},
        headers=auth["headers"],
    )
    assert cleared.json()["data"]["state_id"] is None


async def test_project_state_crud_and_delete_unsets(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    base = f"{API}/orgs/{org['id']}/project-states"
    await client.get(base, headers=auth["headers"])

    created = await client.post(
        base,
        json={"name": "On Hold", "color": "#a16207", "group": "monitoring"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    state_id = created.json()["data"]["id"]

    dupe = await client.post(
        base, json={"name": "On Hold", "group": "monitoring"}, headers=auth["headers"]
    )
    assert dupe.status_code == 409

    project = await create_project(client, auth["headers"], org["id"], key="HLD")
    await client.patch(
        f"{API}/orgs/{org['id']}/projects/{project['id']}",
        json={"state_id": state_id},
        headers=auth["headers"],
    )
    deleted = await client.delete(f"{base}/{state_id}", headers=auth["headers"])
    assert deleted.status_code == 200
    after = await client.get(
        f"{API}/orgs/{org['id']}/projects/{project['id']}", headers=auth["headers"]
    )
    assert after.json()["data"]["state_id"] is None
