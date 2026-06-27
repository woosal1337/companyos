"""Personal access token lifecycle + auth tests."""

from httpx import AsyncClient

from tests.helpers import API, register_and_login


async def test_pat_create_authenticate_revoke(client: AsyncClient) -> None:
    auth = await register_and_login(client)

    created = await client.post(
        f"{API}/users/me/tokens",
        json={"name": "CI token"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    data = created.json()["data"]
    raw = data["token"]
    assert raw.startswith("cos_pat_")
    token_id = data["id"]

    profile = await client.get(f"{API}/users/me", headers={"Authorization": f"Bearer {raw}"})
    assert profile.status_code == 200
    assert profile.json()["data"]["email"] == auth["email"]

    listing = await client.get(f"{API}/users/me/tokens", headers=auth["headers"])
    rows = listing.json()["data"]
    assert len(rows) == 1
    assert "token" not in rows[0]

    revoked = await client.delete(f"{API}/users/me/tokens/{token_id}", headers=auth["headers"])
    assert revoked.status_code == 200

    blocked = await client.get(f"{API}/users/me", headers={"Authorization": f"Bearer {raw}"})
    assert blocked.status_code == 401


async def test_pat_description_and_regenerate(client: AsyncClient) -> None:
    auth = await register_and_login(client)

    created = await client.post(
        f"{API}/users/me/tokens",
        json={"name": "CI", "description": "used by the deploy pipeline"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    data = created.json()["data"]
    assert data["description"] == "used by the deploy pipeline"
    token_id = data["id"]
    old_raw = data["token"]

    assert (await client.get(f"{API}/users/me", headers={"x-api-key": old_raw})).status_code == 200

    regen = await client.post(
        f"{API}/users/me/tokens/{token_id}/regenerate", headers=auth["headers"]
    )
    assert regen.status_code == 200, regen.text
    new_raw = regen.json()["data"]["token"]
    assert new_raw != old_raw
    assert regen.json()["data"]["description"] == "used by the deploy pipeline"

    assert (await client.get(f"{API}/users/me", headers={"x-api-key": old_raw})).status_code == 401
    assert (await client.get(f"{API}/users/me", headers={"x-api-key": new_raw})).status_code == 200
