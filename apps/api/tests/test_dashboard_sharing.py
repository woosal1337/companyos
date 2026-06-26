"""Dashboard private/workspace sharing (COS-134)."""

from httpx import AsyncClient

from tests.helpers import API, add_org_member, create_org, register_and_login


async def test_private_then_publish(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    oh = owner["headers"]
    org = await create_org(client, oh)
    member = await register_and_login(client)
    await add_org_member(client, oh, org["id"], member)
    mh = member["headers"]
    base = f"{API}/orgs/{org['id']}/dashboards"

    dash = await client.post(base, json={"name": "Team metrics"}, headers=oh)
    did = dash.json()["data"]["id"]
    assert dash.json()["data"]["visibility"] == "private"

    assert all(d["id"] != did for d in (await client.get(base, headers=mh)).json()["data"])
    assert (await client.get(f"{base}/{did}", headers=mh)).status_code == 404

    pub = await client.patch(
        f"{base}/{did}/visibility", json={"visibility": "workspace"}, headers=oh
    )
    assert pub.status_code == 200, pub.text
    assert pub.json()["data"]["visibility"] == "workspace"

    assert any(d["id"] == did for d in (await client.get(base, headers=mh)).json()["data"])
    assert (await client.get(f"{base}/{did}", headers=mh)).status_code == 200
    assert (await client.get(f"{base}/{did}/data", headers=mh)).status_code == 200
    assert (
        await client.patch(f"{base}/{did}/visibility", json={"visibility": "private"}, headers=mh)
    ).status_code == 404
    assert (await client.delete(f"{base}/{did}", headers=mh)).status_code == 404

    await client.patch(f"{base}/{did}/visibility", json={"visibility": "private"}, headers=oh)
    assert (await client.get(f"{base}/{did}", headers=mh)).status_code == 404
