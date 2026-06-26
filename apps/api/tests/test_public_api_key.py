"""Public REST API: PAT via x-api-key header (COS-177)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_x_api_key_header_authenticates(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])

    created = await client.post(
        f"{API}/users/me/tokens", json={"name": "API key"}, headers=auth["headers"]
    )
    raw = created.json()["data"]["token"]

    profile = await client.get(f"{API}/users/me", headers={"x-api-key": raw})
    assert profile.status_code == 200, profile.text
    assert profile.json()["data"]["email"] == auth["email"]

    projects = await client.get(f"{API}/orgs/{org['id']}/projects", headers={"x-api-key": raw})
    assert projects.status_code == 200, projects.text

    bad = await client.get(f"{API}/users/me", headers={"x-api-key": "cos_pat_invalid"})
    assert bad.status_code == 401
