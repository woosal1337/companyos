"""Customers CRM-lite (COS-133)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_customer_crud_and_search(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    base = f"{API}/orgs/{org['id']}/customers"

    created = await client.post(
        base,
        json={
            "name": "Acme Corp",
            "email": "ops@acme.test",
            "employees": 250,
            "industry": "Manufacturing",
            "contract_status": "active",
            "revenue": "1500000.00",
        },
        headers=h,
    )
    assert created.status_code == 201, created.text
    customer = created.json()["data"]
    assert customer["contract_status"] == "active"
    assert customer["employees"] == 250

    updated = await client.patch(f"{base}/{customer['id']}", json={"stage": "Expansion"}, headers=h)
    assert updated.json()["data"]["stage"] == "Expansion"

    found = await client.get(f"{base}?search=acme", headers=h)
    assert any(c["id"] == customer["id"] for c in found.json()["data"])

    miss = await client.get(f"{base}?search=zzznotacustomer", headers=h)
    assert all(c["id"] != customer["id"] for c in miss.json()["data"])

    deleted = await client.delete(f"{base}/{customer['id']}", headers=h)
    assert deleted.status_code == 200
