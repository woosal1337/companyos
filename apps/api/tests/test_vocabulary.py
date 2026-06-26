"""Tests for the org vocabulary dictionary."""

from httpx import AsyncClient

from tests.helpers import API, add_org_member, create_org, register_and_login


async def test_vocabulary_crud(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])

    created = await client.post(
        f"{API}/orgs/{org['id']}/vocabulary",
        json={"term": "Pulsar", "definition": "Our realtime sync engine"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    term_id = created.json()["data"]["id"]

    listing = await client.get(f"{API}/orgs/{org['id']}/vocabulary", headers=auth["headers"])
    assert any(item["term"] == "Pulsar" for item in listing.json()["data"])

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/vocabulary/{term_id}",
        json={"definition": "Our realtime sync layer"},
        headers=auth["headers"],
    )
    assert updated.json()["data"]["definition"] == "Our realtime sync layer"

    removed = await client.delete(
        f"{API}/orgs/{org['id']}/vocabulary/{term_id}", headers=auth["headers"]
    )
    assert removed.status_code == 200


async def test_vocabulary_duplicate_rejected(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    await client.post(
        f"{API}/orgs/{org['id']}/vocabulary",
        json={"term": "BYOK", "definition": "Bring your own key"},
        headers=auth["headers"],
    )
    duplicate = await client.post(
        f"{API}/orgs/{org['id']}/vocabulary",
        json={"term": "BYOK", "definition": "again"},
        headers=auth["headers"],
    )
    assert duplicate.status_code == 409


async def test_vocabulary_write_requires_admin(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")

    forbidden = await client.post(
        f"{API}/orgs/{org['id']}/vocabulary",
        json={"term": "Atelier", "definition": "Design tool"},
        headers=member["headers"],
    )
    assert forbidden.status_code == 403

    listing = await client.get(f"{API}/orgs/{org['id']}/vocabulary", headers=member["headers"])
    assert listing.status_code == 200
