"""Customer requests linked to work items (COS-140)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_customer_request_and_task_linkage(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    cbase = f"{API}/orgs/{org['id']}/customers"

    customer = (await client.post(cbase, json={"name": "Acme"}, headers=h)).json()["data"]
    task = await create_task(client, h, org["id"], project["id"])

    created = await client.post(
        f"{cbase}/{customer['id']}/requests",
        json={"title": "SSO support", "status": "planned", "source_url": "https://x.test/1"},
        headers=h,
    )
    assert created.status_code == 201, created.text
    request = created.json()["data"]
    assert request["status"] == "planned"
    assert request["task_ids"] == []

    linked = await client.post(f"{cbase}/requests/{request['id']}/tasks/{task['id']}", headers=h)
    assert linked.status_code == 201, linked.text

    listed = await client.get(f"{cbase}/{customer['id']}/requests", headers=h)
    row = listed.json()["data"][0]
    assert task["id"] in row["task_ids"]

    unlinked = await client.delete(
        f"{cbase}/requests/{request['id']}/tasks/{task['id']}", headers=h
    )
    assert unlinked.status_code == 200

    deleted = await client.delete(f"{cbase}/requests/{request['id']}", headers=h)
    assert deleted.status_code == 200
