"""Seat-billing accounting (COS-207)."""

from httpx import AsyncClient

from tests.helpers import API, add_org_member, create_org, register_and_login


async def test_seat_usage_billable_vs_free(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])

    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    guest = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], guest, role="guest")

    res = await client.get(f"{API}/orgs/{org['id']}/billing/seats", headers=owner["headers"])
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["billable_seats"] == 2
    assert data["free_seats"] == 1
    assert data["total_members"] == 3
    assert data["by_role"]["owner"] == 1
    assert data["by_role"]["guest"] == 1
    assert "member" in data["billable_roles"]
