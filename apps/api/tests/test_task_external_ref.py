"""External-ref provenance + idempotent import upsert (COS-132)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_external_ref_upsert_is_idempotent(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    tasks_url = f"{API}/orgs/{org['id']}/projects/{project['id']}/tasks"

    first = await client.post(
        tasks_url,
        json={"title": "Imported #42", "external_source": "github", "external_id": "42"},
        headers=auth["headers"],
    )
    assert first.status_code == 201, first.text
    data = first.json()["data"]
    assert data["external_source"] == "github"
    assert data["external_id"] == "42"
    task_id = data["id"]

    second = await client.post(
        tasks_url,
        json={
            "title": "Imported #42 (renamed)",
            "status": "in_progress",
            "external_source": "github",
            "external_id": "42",
        },
        headers=auth["headers"],
    )
    assert second.status_code == 201, second.text
    assert second.json()["data"]["id"] == task_id
    assert second.json()["data"]["title"] == "Imported #42 (renamed)"
    assert second.json()["data"]["status"] == "in_progress"

    listing = await client.get(tasks_url, headers=auth["headers"])
    imported = [t for t in listing.json()["data"]["items"] if t["external_id"] == "42"]
    assert len(imported) == 1

    other = await client.post(
        tasks_url,
        json={"title": "Imported #43", "external_source": "github", "external_id": "43"},
        headers=auth["headers"],
    )
    assert other.json()["data"]["id"] != task_id
