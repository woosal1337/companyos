"""User locale preference for i18n (COS-146)."""

from httpx import AsyncClient

from tests.helpers import API, register_and_login


async def test_locale_defaults_and_updates(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]

    me = await client.get(f"{API}/users/me", headers=h)
    assert me.status_code == 200, me.text
    assert me.json()["data"]["locale"] == "en"

    updated = await client.patch(f"{API}/users/me", json={"locale": "es"}, headers=h)
    assert updated.status_code == 200, updated.text
    assert updated.json()["data"]["locale"] == "es"

    again = await client.get(f"{API}/users/me", headers=h)
    assert again.json()["data"]["locale"] == "es"
