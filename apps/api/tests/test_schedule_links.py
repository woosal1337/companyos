"""Scheduling dependencies (COS-68)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_schedule_dependency_crud(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    a = await create_task(client, h, org["id"], project["id"], title="Design")
    b = await create_task(client, h, org["id"], project["id"], title="Build")
    base = f"{API}/orgs/{org['id']}/tasks/{b['id']}/schedule-links"

    created = await client.post(
        base,
        json={
            "other_task_id": a["id"],
            "dependency_type": "finish_to_start",
            "other_is_predecessor": True,
        },
        headers=h,
    )
    assert created.status_code == 201, created.text

    b_links = await client.get(base, headers=h)
    row = b_links.json()["data"][0]
    assert row["task_id"] == a["id"]
    assert row["direction"] == "predecessor"
    assert row["dependency_type"] == "finish_to_start"

    a_links = await client.get(f"{API}/orgs/{org['id']}/tasks/{a['id']}/schedule-links", headers=h)
    assert a_links.json()["data"][0]["direction"] == "successor"

    deleted = await client.delete(f"{base}/{row['link_id']}", headers=h)
    assert deleted.status_code == 200
