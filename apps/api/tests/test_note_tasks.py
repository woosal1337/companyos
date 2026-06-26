"""Reverse page<->work-item linkage (COS-144)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_note_tasks_lists_source_and_linked(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    note = (
        await client.post(
            f"{API}/orgs/{org['id']}/notes",
            json={"title": "Spec", "content": "do things"},
            headers=h,
        )
    ).json()["data"]

    converted = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/tasks",
        json={"title": "Build the thing", "source_note_id": note["id"]},
        headers=h,
    )
    assert converted.status_code == 201, converted.text
    task = converted.json()["data"]

    other = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/tasks",
        json={"title": "Related"},
        headers=h,
    )
    other_id = other.json()["data"]["id"]
    await client.post(f"{API}/orgs/{org['id']}/tasks/{other_id}/notes/{note['id']}", headers=h)

    linked = await client.get(f"{API}/orgs/{org['id']}/notes/{note['id']}/tasks", headers=h)
    assert linked.status_code == 200, linked.text
    ids = {t["id"] for t in linked.json()["data"]}
    assert task["id"] in ids
    assert other_id in ids
