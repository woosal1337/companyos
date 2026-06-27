"""Sticky CRUD tests (per-user scratchpad)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_sticky_crud(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    base = f"{API}/orgs/{org['id']}/stickies"

    created = await client.post(
        base, json={"content": "remember the milk", "color": "pink"}, headers=auth["headers"]
    )
    assert created.status_code == 201, created.text
    sticky = created.json()["data"]
    assert sticky["color"] == "pink"

    updated = await client.patch(
        f"{base}/{sticky['id']}",
        json={"content": "remember oat milk", "color": "green"},
        headers=auth["headers"],
    )
    assert updated.json()["data"]["content"] == "remember oat milk"
    assert updated.json()["data"]["color"] == "green"

    listing = await client.get(base, headers=auth["headers"])
    assert len(listing.json()["data"]) == 1

    deleted = await client.delete(f"{base}/{sticky['id']}", headers=auth["headers"])
    assert deleted.status_code == 200
    empty = await client.get(base, headers=auth["headers"])
    assert empty.json()["data"] == []
