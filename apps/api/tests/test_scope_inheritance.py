"""Scope inheritance: team-derived + team-lead effective project roles (COS-195).

effective_project_role is exercised through the COS-190 role-gated transition
(require_project_role): a team lead resolves to effective ADMIN even though the
grant-on-link only persists a MEMBER row, while a plain team member stays MEMBER.
"""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    create_task,
    register_and_login,
)


async def _me(client: AsyncClient, auth: dict) -> str:
    return (await client.get(f"{API}/users/me", headers=auth["headers"])).json()["data"]["id"]


async def test_team_lead_resolves_to_admin_via_link(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    lead = await register_and_login(client)
    plain = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], lead, role="member")
    await add_org_member(client, owner["headers"], org["id"], plain, role="member")
    lead_id = await _me(client, lead)
    plain_id = await _me(client, plain)

    project = await create_project(client, owner["headers"], org["id"], key="SCP")

    team = (
        await client.post(
            f"{API}/orgs/{org['id']}/teams",
            json={"name": "Inherit", "lead_id": lead_id},
            headers=owner["headers"],
        )
    ).json()["data"]
    await client.post(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/members",
        json={"user_id": plain_id},
        headers=owner["headers"],
    )
    await client.put(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects",
        json={"project_ids": [project["id"]]},
        headers=owner["headers"],
    )

    members = (
        await client.get(
            f"{API}/orgs/{org['id']}/projects/{project['id']}/members", headers=owner["headers"]
        )
    ).json()["data"]
    roles = {m["user_id"]: m["role"] for m in members}
    assert roles[lead_id] == "member"
    assert roles[plain_id] == "member"

    statuses = (
        await client.get(f"{API}/orgs/{org['id']}/workflow/statuses", headers=owner["headers"])
    ).json()["data"]
    by_name = {s["name"]: s["id"] for s in statuses}
    await client.post(
        f"{API}/orgs/{org['id']}/workflow/transitions",
        json={
            "from_status_id": by_name["Backlog"],
            "to_status_id": by_name["Todo"],
            "required_role": "admin",
        },
        headers=owner["headers"],
    )

    task = await create_task(client, owner["headers"], org["id"], project["id"])

    blocked = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "todo"},
        headers=plain["headers"],
    )
    assert blocked.status_code == 403, blocked.text

    allowed = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "todo"},
        headers=lead["headers"],
    )
    assert allowed.status_code == 200, allowed.text
