"""Granular access: custom roles from permission schemes (COS-176)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_custom_role_lifecycle_and_permissions(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    base = f"{API}/orgs/{org['id']}/roles"

    perms = await client.get(f"{base}/permissions", headers=h)
    assert perms.status_code == 200, perms.text
    data = perms.json()["data"]
    assert len(data["catalog"]) >= 10
    assert "billing.manage" in data["granted"]

    created = await client.post(
        base,
        json={"name": "Editor", "permissions": ["tasks.create", "tasks.assign", "bogus.perm"]},
        headers=h,
    )
    assert created.status_code == 201, created.text
    role = created.json()["data"]
    assert set(role["permissions"]) == {"tasks.create", "tasks.assign"}

    dup = await client.post(base, json={"name": "Editor", "permissions": []}, headers=h)
    assert dup.status_code == 409

    listed = await client.get(base, headers=h)
    assert any(r["name"] == "Editor" for r in listed.json()["data"])

    upd = await client.patch(
        f"{base}/{role['id']}", json={"permissions": ["tasks.create"]}, headers=h
    )
    assert upd.json()["data"]["permissions"] == ["tasks.create"]

    assert (await client.delete(f"{base}/{role['id']}", headers=h)).status_code == 200
