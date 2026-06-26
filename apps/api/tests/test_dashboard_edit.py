"""Dashboard widget span + reorder (COS-145)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_widget_span_and_reorder(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    base = f"{API}/orgs/{org['id']}/dashboards"
    did = (await client.post(base, json={"name": "D"}, headers=h)).json()["data"]["id"]

    w = await client.post(
        f"{base}/{did}/widgets",
        json={
            "title": "Wide",
            "config": {"chart_type": "bar", "metric": "count", "dimension": "status", "span": 2},
        },
        headers=h,
    )
    assert w.json()["data"]["config"]["span"] == 2
    wid = w.json()["data"]["id"]

    upd = await client.patch(f"{base}/{did}/widgets/{wid}", json={"position": 3}, headers=h)
    assert upd.json()["data"]["position"] == 3

    fav = await client.post(
        f"{API}/orgs/{org['id']}/favorites",
        json={"entity_type": "dashboard", "entity_id": did, "label": "D"},
        headers=h,
    )
    assert fav.status_code in (200, 201), fav.text
    favs = await client.get(f"{API}/orgs/{org['id']}/favorites", headers=h)
    assert any(f["entity_id"] == did for f in favs.json()["data"])
