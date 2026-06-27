"""Organization, membership, and invitation tests."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    register_and_login,
)


async def test_create_org_creator_is_owner(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"], name="Owner Org")
    listing = await client.get(f"{API}/orgs", headers=auth["headers"])
    assert listing.status_code == 200
    assert [o["id"] for o in listing.json()["data"]] == [org["id"]]
    members = await client.get(f"{API}/orgs/{org['id']}/members", headers=auth["headers"])
    assert members.status_code == 200
    rows = members.json()["data"]
    assert len(rows) == 1
    assert rows[0]["role"] == "owner"
    assert rows[0]["user_id"] == auth["user_id"]


async def test_update_org_requires_admin(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    forbidden = await client.patch(
        f"{API}/orgs/{org['id']}", json={"name": "Hacked"}, headers=member["headers"]
    )
    assert forbidden.status_code == 403
    allowed = await client.patch(
        f"{API}/orgs/{org['id']}", json={"name": "Renamed"}, headers=owner["headers"]
    )
    assert allowed.status_code == 200
    assert allowed.json()["data"]["name"] == "Renamed"


async def test_invite_accept_flow(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    invitee = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    invite = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": invitee["email"], "role": "admin"},
        headers=owner["headers"],
    )
    assert invite.status_code == 201
    token = invite.json()["data"]["token"]
    assert token
    accept = await client.post(
        f"{API}/invites/accept", json={"token": token}, headers=invitee["headers"]
    )
    assert accept.status_code == 200
    assert accept.json()["data"]["id"] == org["id"]
    members = await client.get(f"{API}/orgs/{org['id']}/members", headers=invitee["headers"])
    assert members.status_code == 200
    roles = {row["user_id"]: row["role"] for row in members.json()["data"]}
    assert roles[invitee["user_id"]] == "admin"
    listing = await client.get(f"{API}/orgs/{org['id']}/invites", headers=owner["headers"])
    assert listing.json()["data"][0]["status"] == "accepted"
    assert listing.json()["data"][0]["token"] is None


async def test_project_scoped_invite_joins_org_and_project(client: AsyncClient) -> None:
    """End-to-end: invite a user to a project, accept, and verify org + project join."""
    owner = await register_and_login(client)
    invitee = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    project = await create_project(client, owner["headers"], org["id"], key="HML", name="Hammal")

    invite = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": invitee["email"], "role": "member", "project_id": project["id"]},
        headers=owner["headers"],
    )
    assert invite.status_code == 201, invite.text
    body = invite.json()["data"]
    assert body["project_id"] == project["id"]
    token = body["token"]
    assert token

    accept = await client.post(
        f"{API}/invites/accept", json={"token": token}, headers=invitee["headers"]
    )
    assert accept.status_code == 200, accept.text

    members = await client.get(f"{API}/orgs/{org['id']}/members", headers=invitee["headers"])
    assert members.status_code == 200
    assert invitee["user_id"] in {row["user_id"] for row in members.json()["data"]}

    proj_members = await client.get(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members", headers=invitee["headers"]
    )
    assert proj_members.status_code == 200, proj_members.text
    assert invitee["user_id"] in {row["user_id"] for row in proj_members.json()["data"]}


async def test_invite_rejects_project_from_another_org(client: AsyncClient) -> None:
    """A project_id must belong to the inviting org, or the invite is rejected."""
    owner = await register_and_login(client)
    other = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    other_org = await create_org(client, other["headers"], name="Other Co")
    foreign = await create_project(
        client, other["headers"], other_org["id"], key="OTH", name="Foreign"
    )
    bad = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": "stranger@test.dev", "role": "member", "project_id": foreign["id"]},
        headers=owner["headers"],
    )
    assert bad.status_code == 400, bad.text


async def test_invite_revoke(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    invite = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": "ghost@test.dev"},
        headers=owner["headers"],
    )
    invite_id = invite.json()["data"]["id"]
    revoke = await client.delete(
        f"{API}/orgs/{org['id']}/invites/{invite_id}", headers=owner["headers"]
    )
    assert revoke.status_code == 200
    listing = await client.get(f"{API}/orgs/{org['id']}/invites", headers=owner["headers"])
    assert listing.json()["data"][0]["status"] == "revoked"


async def test_member_role_update_and_last_owner_guard(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member)
    promote = await client.patch(
        f"{API}/orgs/{org['id']}/members/{member['user_id']}",
        json={"role": "admin"},
        headers=owner["headers"],
    )
    assert promote.status_code == 200
    demote_last_owner = await client.patch(
        f"{API}/orgs/{org['id']}/members/{owner['user_id']}",
        json={"role": "member"},
        headers=owner["headers"],
    )
    assert demote_last_owner.status_code == 403
    remove = await client.delete(
        f"{API}/orgs/{org['id']}/members/{member['user_id']}", headers=owner["headers"]
    )
    assert remove.status_code == 200
    members = await client.get(f"{API}/orgs/{org['id']}/members", headers=owner["headers"])
    assert len(members.json()["data"]) == 1


async def test_admin_cannot_promote_member_to_owner(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    admin = await register_and_login(client)
    target = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    await add_org_member(client, owner["headers"], org["id"], target, role="member")
    forbidden = await client.patch(
        f"{API}/orgs/{org['id']}/members/{target['user_id']}",
        json={"role": "owner"},
        headers=admin["headers"],
    )
    assert forbidden.status_code == 403


async def test_admin_cannot_self_promote_to_owner(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    forbidden = await client.patch(
        f"{API}/orgs/{org['id']}/members/{admin['user_id']}",
        json={"role": "owner"},
        headers=admin["headers"],
    )
    assert forbidden.status_code == 403


async def test_admin_cannot_demote_or_remove_owner(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    second_owner = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], second_owner, role="owner")
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    demote = await client.patch(
        f"{API}/orgs/{org['id']}/members/{second_owner['user_id']}",
        json={"role": "member"},
        headers=admin["headers"],
    )
    assert demote.status_code == 403
    remove = await client.delete(
        f"{API}/orgs/{org['id']}/members/{second_owner['user_id']}", headers=admin["headers"]
    )
    assert remove.status_code == 403


async def test_admin_cannot_invite_as_owner(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    forbidden = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": "outsider@test.dev", "role": "owner"},
        headers=admin["headers"],
    )
    assert forbidden.status_code == 403


async def test_owner_can_manage_owner_level(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    second_owner = await register_and_login(client)
    target = await register_and_login(client)
    invitee = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], second_owner, role="owner")
    await add_org_member(client, owner["headers"], org["id"], target, role="member")
    promote = await client.patch(
        f"{API}/orgs/{org['id']}/members/{target['user_id']}",
        json={"role": "owner"},
        headers=owner["headers"],
    )
    assert promote.status_code == 200
    demote = await client.patch(
        f"{API}/orgs/{org['id']}/members/{second_owner['user_id']}",
        json={"role": "member"},
        headers=owner["headers"],
    )
    assert demote.status_code == 200
    remove = await client.delete(
        f"{API}/orgs/{org['id']}/members/{target['user_id']}", headers=owner["headers"]
    )
    assert remove.status_code == 200
    invite = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": invitee["email"], "role": "owner"},
        headers=owner["headers"],
    )
    assert invite.status_code == 201


async def test_owner_invite_last_owner_guard_holds(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    demote_last_owner = await client.patch(
        f"{API}/orgs/{org['id']}/members/{owner['user_id']}",
        json={"role": "member"},
        headers=owner["headers"],
    )
    assert demote_last_owner.status_code == 403


async def test_admin_cannot_change_own_role(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    self_demote = await client.patch(
        f"{API}/orgs/{org['id']}/members/{admin['user_id']}",
        json={"role": "member"},
        headers=admin["headers"],
    )
    assert self_demote.status_code == 403
    assert self_demote.json()["message"] == "You cannot change your own role"


async def test_owner_cannot_self_demote_with_second_owner(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    second_owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], second_owner, role="owner")
    self_demote = await client.patch(
        f"{API}/orgs/{org['id']}/members/{owner['user_id']}",
        json={"role": "member"},
        headers=owner["headers"],
    )
    assert self_demote.status_code == 403
    assert self_demote.json()["message"] == "You cannot change your own role"


async def test_remove_member_cascades_team_and_project_memberships(
    client: AsyncClient,
) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    team = await client.post(
        f"{API}/orgs/{org['id']}/teams",
        json={"name": "Platform"},
        headers=owner["headers"],
    )
    assert team.status_code == 201, team.text
    team_id = team.json()["data"]["id"]
    add_team = await client.post(
        f"{API}/orgs/{org['id']}/teams/{team_id}/members",
        json={"user_id": member["user_id"]},
        headers=owner["headers"],
    )
    assert add_team.status_code == 201, add_team.text
    project = await create_project(client, owner["headers"], org["id"])
    add_project = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members",
        json={"user_id": member["user_id"]},
        headers=owner["headers"],
    )
    assert add_project.status_code == 201, add_project.text
    remove = await client.delete(
        f"{API}/orgs/{org['id']}/members/{member['user_id']}", headers=owner["headers"]
    )
    assert remove.status_code == 200
    team_members = await client.get(
        f"{API}/orgs/{org['id']}/teams/{team_id}/members", headers=owner["headers"]
    )
    assert team_members.status_code == 200
    assert member["user_id"] not in [m["user_id"] for m in team_members.json()["data"]]
    project_members = await client.get(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members", headers=owner["headers"]
    )
    assert project_members.status_code == 200
    assert member["user_id"] not in [m["user_id"] for m in project_members.json()["data"]]


async def test_accept_invite_requires_matching_email(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    intended = await register_and_login(client)
    intruder = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    invite = await client.post(
        f"{API}/orgs/{org['id']}/invites",
        json={"email": intended["email"], "role": "member"},
        headers=owner["headers"],
    )
    assert invite.status_code == 201
    token = invite.json()["data"]["token"]
    wrong = await client.post(
        f"{API}/invites/accept", json={"token": token}, headers=intruder["headers"]
    )
    assert wrong.status_code == 403
    correct = await client.post(
        f"{API}/invites/accept", json={"token": token}, headers=intended["headers"]
    )
    assert correct.status_code == 200
    assert correct.json()["data"]["id"] == org["id"]
