"""SCIM 2.0 provisioning (COS-184)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_scim_provisioning(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)

    minted = await client.post(f"{API}/orgs/{org['id']}/scim/token", headers=h)
    assert minted.status_code == 200, minted.text
    token = minted.json()["data"]["token"]
    assert token.startswith("scim_")
    scim_h = {"Authorization": f"Bearer {token}"}
    base = f"{API}/scim/v2/orgs/{org['id']}"

    assert (await client.get(f"{base}/Users")).status_code == 401

    created = await client.post(
        f"{base}/Users",
        json={
            "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
            "userName": "alice@acme.com",
            "name": {"givenName": "Alice", "familyName": "Smith"},
            "emails": [{"value": "alice@acme.com", "primary": True}],
            "active": True,
        },
        headers=scim_h,
    )
    assert created.status_code == 201, created.text
    uid = created.json()["id"]
    assert created.json()["active"] is True
    assert created.json()["userName"] == "alice@acme.com"

    listed = await client.get(f"{base}/Users", headers=scim_h)
    assert listed.json()["totalResults"] >= 2

    got = await client.get(f"{base}/Users/{uid}", headers=scim_h)
    assert got.json()["userName"] == "alice@acme.com"

    patched = await client.patch(
        f"{base}/Users/{uid}",
        json={"Operations": [{"op": "replace", "path": "active", "value": False}]},
        headers=scim_h,
    )
    assert patched.status_code == 200, patched.text
    assert patched.json()["active"] is False
    assert (await client.get(f"{base}/Users/{uid}", headers=scim_h)).status_code == 404

    await client.delete(f"{API}/orgs/{org['id']}/scim/token", headers=h)
    assert (await client.get(f"{base}/Users", headers=scim_h)).status_code == 401
