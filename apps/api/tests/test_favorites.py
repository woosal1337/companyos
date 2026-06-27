"""Favorites lifecycle tests."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_favorites_pin_list_unpin(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="FAV")
    base = f"{API}/orgs/{org['id']}/favorites"

    pinned = await client.post(
        base,
        json={"entity_type": "project", "entity_id": project["id"], "label": project["name"]},
        headers=auth["headers"],
    )
    assert pinned.status_code == 201, pinned.text

    again = await client.post(
        base,
        json={"entity_type": "project", "entity_id": project["id"], "label": "Renamed"},
        headers=auth["headers"],
    )
    assert again.status_code == 201

    listing = await client.get(base, headers=auth["headers"])
    rows = listing.json()["data"]
    assert len(rows) == 1
    assert rows[0]["label"] == "Renamed"

    removed = await client.delete(f"{base}/project/{project['id']}", headers=auth["headers"])
    assert removed.status_code == 200
    empty = await client.get(base, headers=auth["headers"])
    assert empty.json()["data"] == []
