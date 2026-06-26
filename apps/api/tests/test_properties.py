"""Custom property definition + task value tests."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_custom_property_crud_and_task_values(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CPR")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/properties"

    created = await client.post(
        base,
        json={"name": "Team", "type": "select", "options": ["Platform", "Growth"]},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    prop = created.json()["data"]
    assert prop["type"] == "select"
    assert prop["options"] == ["Platform", "Growth"]

    listing = await client.get(base, headers=auth["headers"])
    assert len(listing.json()["data"]) == 1

    task = await create_task(client, auth["headers"], org["id"], project["id"])
    updated = await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}",
        json={"custom_fields": {prop["id"]: "Platform"}},
        headers=auth["headers"],
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["data"]["custom_fields"] == {prop["id"]: "Platform"}

    deleted = await client.delete(f"{base}/{prop['id']}", headers=auth["headers"])
    assert deleted.status_code == 200


async def test_select_property_requires_options(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CPS")
    response = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/properties",
        json={"name": "Stage", "type": "select", "options": []},
        headers=auth["headers"],
    )
    assert response.status_code == 400
