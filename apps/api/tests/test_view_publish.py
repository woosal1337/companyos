"""Publish a view to a public login-less link (COS-167)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_publish_and_read_public_view(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    await create_task(client, h, org["id"], project["id"], title="Public task")

    view = await client.post(
        f"{API}/orgs/{org['id']}/views",
        json={"name": "Everything", "config": {}},
        headers=h,
    )
    view_id = view.json()["data"]["id"]

    published = await client.post(f"{API}/orgs/{org['id']}/views/{view_id}/publish", headers=h)
    assert published.status_code == 200, published.text
    token = published.json()["data"]["public_token"]
    assert token

    public = await client.get(f"{API}/public/views/{token}")
    assert public.status_code == 200, public.text
    body = public.json()["data"]
    assert body["name"] == "Everything"
    assert any(t["title"] == "Public task" for t in body["tasks"])
    assert set(body["tasks"][0].keys()) == {"identifier", "title", "status", "priority"}

    await client.delete(f"{API}/orgs/{org['id']}/views/{view_id}/publish", headers=h)
    gone = await client.get(f"{API}/public/views/{token}")
    assert gone.status_code == 404
