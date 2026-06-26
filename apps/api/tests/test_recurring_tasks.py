"""Recurring work items (COS-143)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_recurring_rule_run_now(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    created = await client.post(
        f"{pbase}/recurring-tasks",
        json={"title": "Weekly audit", "interval_days": 7},
        headers=h,
    )
    assert created.status_code == 201, created.text
    rule = created.json()["data"]
    assert rule["interval_days"] == 7
    first_next = rule["next_run_at"]

    ran = await client.post(f"{API}/orgs/{org['id']}/recurring-tasks/{rule['id']}/run", headers=h)
    assert ran.status_code == 201, ran.text

    listed = await client.get(f"{pbase}/recurring-tasks", headers=h)
    refreshed = listed.json()["data"][0]
    assert refreshed["last_run_at"] is not None
    assert refreshed["next_run_at"] > first_next

    board = await client.get(f"{pbase}/tasks?search=Weekly%20audit", headers=h)
    assert board.json()["data"]["total"] >= 1

    await client.patch(
        f"{API}/orgs/{org['id']}/recurring-tasks/{rule['id']}",
        json={"active": False},
        headers=h,
    )
    deleted = await client.delete(f"{API}/orgs/{org['id']}/recurring-tasks/{rule['id']}", headers=h)
    assert deleted.status_code == 200
