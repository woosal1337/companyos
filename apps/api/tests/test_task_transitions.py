"""Task status-transition history + time-in-state (COS-153)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_task_transitions(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    task = await create_task(client, auth["headers"], org["id"], project["id"])
    base = f"{API}/orgs/{org['id']}/tasks/{task['id']}"

    for status in ("in_progress", "done"):
        await client.post(f"{base}/status", json={"status": status}, headers=auth["headers"])

    transitions = await client.get(f"{base}/transitions", headers=auth["headers"])
    assert transitions.status_code == 200, transitions.text
    data = transitions.json()["data"]
    assert data["current_status"] == "done"
    assert data["seconds_in_current"] >= 0
    assert isinstance(data["transitions"], list)
    assert all(
        {"from_status", "to_status", "at", "seconds_in_prev"} <= set(t) for t in data["transitions"]
    )
