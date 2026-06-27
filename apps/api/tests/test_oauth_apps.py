"""Confidential OAuth apps + client_credentials bot tokens (COS-198)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_oauth_app_client_credentials_bot_token(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)

    created = await client.post(f"{API}/oauth/apps", json={"name": "My Automation"}, headers=h)
    assert created.status_code == 201, created.text
    app = created.json()["data"]
    assert app["client_id"].startswith("app-")
    assert app["client_secret"].startswith("cos_secret_")

    listed = await client.get(f"{API}/oauth/apps", headers=h)
    assert any(a["client_id"] == app["client_id"] for a in listed.json()["data"])

    token_res = await client.post(
        f"{API}/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": app["client_id"],
            "client_secret": app["client_secret"],
        },
    )
    assert token_res.status_code == 200, token_res.text
    bot_token = token_res.json()["access_token"]

    me = await client.get(f"{API}/users/me", headers={"x-api-key": bot_token})
    assert me.status_code == 200
    assert me.json()["data"]["email"] == auth["email"]
    projects = await client.get(
        f"{API}/orgs/{org['id']}/projects", headers={"x-api-key": bot_token}
    )
    assert projects.status_code == 200

    bad = await client.post(
        f"{API}/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": app["client_id"],
            "client_secret": "cos_secret_wrong",
        },
    )
    assert bad.status_code == 400

    await client.delete(f"{API}/oauth/apps/{app['client_id']}", headers=h)
    after = await client.post(
        f"{API}/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": app["client_id"],
            "client_secret": app["client_secret"],
        },
    )
    assert after.status_code == 400
