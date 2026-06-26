"""Task approval flow tests (COS-215)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_approval_request_approve_applies_transition(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="APP")
    task = await create_task(client, auth["headers"], org["id"], project["id"])
    base = f"{API}/orgs/{org['id']}/tasks/{task['id']}/approvals"

    requested = await client.post(base, json={"target_status": "done"}, headers=auth["headers"])
    assert requested.status_code == 201, requested.text
    approval = requested.json()["data"]
    assert approval["state"] == "pending"

    dup = await client.post(base, json={"target_status": "todo"}, headers=auth["headers"])
    assert dup.status_code == 409

    approved = await client.post(f"{base}/{approval['id']}/approve", headers=auth["headers"])
    assert approved.status_code == 200, approved.text
    assert approved.json()["data"]["state"] == "approved"

    fetched = await client.get(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    assert fetched.json()["data"]["status"] == "done"


async def test_approval_reject_leaves_status(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="APR")
    task = await create_task(client, auth["headers"], org["id"], project["id"])
    base = f"{API}/orgs/{org['id']}/tasks/{task['id']}/approvals"

    approval = (
        await client.post(base, json={"target_status": "in_progress"}, headers=auth["headers"])
    ).json()["data"]
    rejected = await client.post(
        f"{base}/{approval['id']}/reject",
        json={"note": "not yet"},
        headers=auth["headers"],
    )
    assert rejected.status_code == 200, rejected.text
    assert rejected.json()["data"]["state"] == "rejected"

    fetched = await client.get(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    assert fetched.json()["data"]["status"] == "backlog"

    again = await client.post(f"{base}/{approval['id']}/approve", headers=auth["headers"])
    assert again.status_code == 409
