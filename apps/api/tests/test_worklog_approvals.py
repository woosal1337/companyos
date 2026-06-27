"""Worklog approvals (COS-185)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_worklog_approval_flow(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="APR")
    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Build")
    base = f"{API}/orgs/{org['id']}"

    auto = await client.post(
        f"{base}/tasks/{task['id']}/worklogs", json={"minutes": 30}, headers=auth["headers"]
    )
    assert auto.json()["data"]["approval_status"] == "approved"

    await client.patch(
        f"{base}/projects/{project['id']}",
        json={"worklog_approval_required": True},
        headers=auth["headers"],
    )

    pending = await client.post(
        f"{base}/tasks/{task['id']}/worklogs", json={"minutes": 90}, headers=auth["headers"]
    )
    worklog_id = pending.json()["data"]["id"]
    assert pending.json()["data"]["approval_status"] == "pending"

    queue = await client.get(
        f"{base}/projects/{project['id']}/worklogs/pending", headers=auth["headers"]
    )
    assert [w["id"] for w in queue.json()["data"]] == [worklog_id]

    approved = await client.post(
        f"{base}/worklogs/{worklog_id}/approve",
        json={"note": "ok"},
        headers=auth["headers"],
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["data"]["approval_status"] == "approved"
    assert approved.json()["data"]["approver_id"]
    assert approved.json()["data"]["decision_note"] == "ok"

    queue2 = await client.get(
        f"{base}/projects/{project['id']}/worklogs/pending", headers=auth["headers"]
    )
    assert queue2.json()["data"] == []
