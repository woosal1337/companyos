"""Agents as non-billable bot users + bot task assignment (COS-272)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_bots_are_non_billable_and_assignable(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)

    seats = await client.get(f"{API}/orgs/{org['id']}/billing/seats", headers=h)
    assert seats.status_code == 200, seats.text
    assert seats.json()["data"]["billable_seats"] == 1
    assert seats.json()["data"]["bot_users"] == 0

    bot = await client.post(
        f"{API}/orgs/{org['id']}/ai/users",
        json={
            "name": "Triage Bot",
            "provider": "openai",
            "model": "gpt-4o",
            "system_prompt": "Triage incoming work.",
        },
        headers=h,
    )
    assert bot.status_code == 201, bot.text
    bot_id = bot.json()["data"]["id"]

    seats2 = await client.get(f"{API}/orgs/{org['id']}/billing/seats", headers=h)
    assert seats2.json()["data"]["billable_seats"] == 1
    assert seats2.json()["data"]["bot_users"] == 1

    edition = await client.get(f"{API}/orgs/{org['id']}/billing/edition", headers=h)
    assert edition.json()["data"]["bot_users"] == 1
    assert edition.json()["data"]["billable_seats"] == 1

    project = await create_project(client, h, org["id"], key="BOT")
    task = await create_task(client, h, org["id"], project["id"], title="Auto-triage me")
    assigned = await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}",
        json={"bot_assignee_id": bot_id},
        headers=h,
    )
    assert assigned.status_code == 200, assigned.text
    assert assigned.json()["data"]["bot_assignee_id"] == bot_id

    cleared = await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}",
        json={"clear_bot_assignee": True},
        headers=h,
    )
    assert cleared.json()["data"]["bot_assignee_id"] is None
