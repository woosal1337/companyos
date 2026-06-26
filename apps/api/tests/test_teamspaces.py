"""Teamspace lead, charter, and project-link grants (COS-37)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    register_and_login,
)


async def _me(client: AsyncClient, auth: dict) -> str:
    return (await client.get(f"{API}/users/me", headers=auth["headers"])).json()["data"]["id"]


async def _members(client: AsyncClient, owner: dict, org_id: str, project_id: str) -> dict:
    resp = await client.get(
        f"{API}/orgs/{org_id}/projects/{project_id}/members", headers=owner["headers"]
    )
    return {m["user_id"]: m["role"] for m in resp.json()["data"]}


async def test_create_teamspace_with_lead_charter_logo(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    lead = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], lead, role="member")
    lead_id = await _me(client, lead)

    created = await client.post(
        f"{API}/orgs/{org['id']}/teams",
        json={
            "name": "Platform",
            "lead_id": lead_id,
            "charter": "# Mission\nOwn the platform.",
            "logo_props": {"icon": "rocket", "color": "accent"},
        },
        headers=owner["headers"],
    )
    assert created.status_code == 201, created.text
    team = created.json()["data"]
    assert team["lead_id"] == lead_id
    assert team["charter"].startswith("# Mission")
    assert team["logo_props"] == {"icon": "rocket", "color": "accent"}

    members = await client.get(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/members", headers=owner["headers"]
    )
    assert lead_id in {m["user_id"] for m in members.json()["data"]}


async def test_lead_must_be_org_member(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    outsider = await register_and_login(client)
    outsider_id = await _me(client, outsider)
    blocked = await client.post(
        f"{API}/orgs/{org['id']}/teams",
        json={"name": "Bad", "lead_id": outsider_id},
        headers=owner["headers"],
    )
    assert blocked.status_code == 400, blocked.text


async def test_lead_gating_for_settings(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    lead = await register_and_login(client)
    other = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], lead, role="member")
    await add_org_member(client, owner["headers"], org["id"], other, role="member")
    lead_id = await _me(client, lead)

    team = (
        await client.post(
            f"{API}/orgs/{org['id']}/teams",
            json={"name": "Eng", "lead_id": lead_id},
            headers=owner["headers"],
        )
    ).json()["data"]
    base = f"{API}/orgs/{org['id']}/teams/{team['id']}"

    as_lead = await client.patch(base, json={"description": "ours"}, headers=lead["headers"])
    assert as_lead.status_code == 200, as_lead.text
    as_other = await client.patch(base, json={"description": "nope"}, headers=other["headers"])
    assert as_other.status_code == 403, as_other.text
    as_admin = await client.patch(base, json={"description": "admin"}, headers=owner["headers"])
    assert as_admin.status_code == 200, as_admin.text


async def test_linking_project_grants_members_and_preserves_admin(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    admin_member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    await add_org_member(client, owner["headers"], org["id"], admin_member, role="member")
    member_id = await _me(client, member)
    admin_id = await _me(client, admin_member)

    project = await create_project(client, owner["headers"], org["id"], key="LNK")
    await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members",
        json={"user_id": admin_id, "role": "admin"},
        headers=owner["headers"],
    )

    team = (
        await client.post(
            f"{API}/orgs/{org['id']}/teams", json={"name": "Squad"}, headers=owner["headers"]
        )
    ).json()["data"]
    for uid in (member_id, admin_id):
        await client.post(
            f"{API}/orgs/{org['id']}/teams/{team['id']}/members",
            json={"user_id": uid},
            headers=owner["headers"],
        )

    linked = await client.put(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects",
        json={"project_ids": [project["id"]]},
        headers=owner["headers"],
    )
    assert linked.status_code == 200, linked.text

    roles = await _members(client, owner, org["id"], project["id"])
    assert roles[member_id] == "member"
    assert roles[admin_id] == "admin"

    again = await client.put(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects",
        json={"project_ids": [project["id"]]},
        headers=owner["headers"],
    )
    assert again.status_code == 200, again.text

    listed = await client.get(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects", headers=owner["headers"]
    )
    assert {p["id"] for p in listed.json()["data"]} == {project["id"]}


async def test_late_joiner_gains_access_and_unlink_is_sticky(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    member_id = await _me(client, member)
    project = await create_project(client, owner["headers"], org["id"], key="LATE")

    team = (
        await client.post(
            f"{API}/orgs/{org['id']}/teams", json={"name": "Ops"}, headers=owner["headers"]
        )
    ).json()["data"]
    await client.put(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects",
        json={"project_ids": [project["id"]]},
        headers=owner["headers"],
    )
    await client.post(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/members",
        json={"user_id": member_id},
        headers=owner["headers"],
    )
    assert (await _members(client, owner, org["id"], project["id"])).get(member_id) == "member"

    unlinked = await client.request(
        "DELETE",
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects",
        json={"project_ids": [project["id"]]},
        headers=owner["headers"],
    )
    assert unlinked.status_code == 200, unlinked.text
    assert (await _members(client, owner, org["id"], project["id"])).get(member_id) == "member"
    listed = await client.get(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects", headers=owner["headers"]
    )
    assert listed.json()["data"] == []
