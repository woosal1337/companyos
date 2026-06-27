"""Per-seat AI credit pool usage (COS-264)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_ai_usage_pool(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)

    res = await client.get(f"{API}/orgs/{org['id']}/ai/usage", headers=h)
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["billable_seats"] == 1
    assert data["credits_per_seat"] == 500
    assert data["limit"] == 500
    assert data["used"] == 0
    assert data["remaining"] == 500
    assert data["percent_used"] == 0.0
