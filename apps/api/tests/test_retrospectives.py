"""Retrospectives (COS-267)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_retrospective_crud(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    created = await client.post(
        f"{pbase}/retrospectives",
        json={"title": "Sprint 1 retro", "went_well": "Shipped on time", "to_improve": "Less WIP"},
        headers=h,
    )
    assert created.status_code == 201, created.text
    retro = created.json()["data"]
    assert retro["went_well"] == "Shipped on time"

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/retrospectives/{retro['id']}",
        json={"action_items": "Add WIP limit"},
        headers=h,
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["action_items"] == "Add WIP limit"

    listed = await client.get(f"{pbase}/retrospectives", headers=h)
    assert len(listed.json()["data"]) == 1

    deleted = await client.delete(f"{API}/orgs/{org['id']}/retrospectives/{retro['id']}", headers=h)
    assert deleted.status_code == 200
