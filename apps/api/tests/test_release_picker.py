"""Release picker on work items (COS-97)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_set_release_on_task(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    task = await create_task(client, h, org["id"], project["id"])

    release = (
        await client.post(f"{API}/orgs/{org['id']}/releases", json={"name": "v2.0"}, headers=h)
    ).json()["data"]

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}",
        json={"release_id": release["id"]},
        headers=h,
    )
    assert updated.status_code == 200, updated.text
    assert updated.json()["data"]["release_id"] == release["id"]

    scope = await client.get(f"{API}/orgs/{org['id']}/releases/{release['id']}/tasks", headers=h)
    assert any(t["id"] == task["id"] for t in scope.json()["data"])

    cleared = await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}",
        json={"clear_release": True},
        headers=h,
    )
    assert cleared.json()["data"]["release_id"] is None
