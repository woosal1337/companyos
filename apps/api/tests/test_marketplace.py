"""Marketplace catalog + installed (COS-273)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_marketplace_catalog(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    base = f"{API}/orgs/{org['id']}/marketplace"

    catalog = await client.get(f"{base}/catalog", headers=h)
    assert catalog.status_code == 200, catalog.text
    items = catalog.json()["data"]
    cats = {i["category"] for i in items}
    assert {"app", "agent", "importer", "connector"} <= cats

    connectors = await client.get(f"{base}/catalog", params={"category": "connector"}, headers=h)
    assert all(i["category"] == "connector" for i in connectors.json()["data"])
    assert len(connectors.json()["data"]) >= 1

    one = await client.get(f"{base}/catalog/ai-agent", headers=h)
    assert one.json()["data"]["category"] == "agent"
    assert (await client.get(f"{base}/catalog/nope", headers=h)).status_code == 404

    inst = await client.get(f"{base}/installed", headers=h)
    assert inst.json()["data"]["connectors"] == 0
    assert "categories" in inst.json()["data"]
