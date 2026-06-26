"""Teamspace-scoped views: union dataset + membership gating (COS-69)."""

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


async def _setup_team_with_two_projects(client: AsyncClient, owner: dict, org_id: str) -> dict:
    pa = await create_project(client, owner["headers"], org_id, key="TVA")
    pb = await create_project(client, owner["headers"], org_id, key="TVB")
    await create_task(client, owner["headers"], org_id, pa["id"], title="A-one")
    await create_task(client, owner["headers"], org_id, pb["id"], title="B-one")
    team = (
        await client.post(
            f"{API}/orgs/{org_id}/teams", json={"name": "Delivery"}, headers=owner["headers"]
        )
    ).json()["data"]
    await client.put(
        f"{API}/orgs/{org_id}/teams/{team['id']}/projects",
        json={"project_ids": [pa["id"], pb["id"]]},
        headers=owner["headers"],
    )
    return {"team": team, "pa": pa, "pb": pb}


async def test_teamspace_view_requires_team_id(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    rejected = await client.post(
        f"{API}/orgs/{org['id']}/views",
        json={"name": "No team", "scope": "teamspace"},
        headers=owner["headers"],
    )
    assert rejected.status_code == 422, rejected.text


async def test_teamspace_view_unions_linked_projects(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    setup = await _setup_team_with_two_projects(client, owner, org["id"])

    view = (
        await client.post(
            f"{API}/orgs/{org['id']}/views",
            json={"name": "All delivery", "scope": "teamspace", "team_id": setup["team"]["id"]},
            headers=owner["headers"],
        )
    ).json()["data"]
    assert view["scope"] == "teamspace"
    assert view["team_id"] == setup["team"]["id"]

    tasks = await client.get(
        f"{API}/orgs/{org['id']}/views/{view['id']}/tasks", headers=owner["headers"]
    )
    assert tasks.status_code == 200, tasks.text
    titles = {t["title"] for t in tasks.json()["data"]}
    assert titles == {"A-one", "B-one"}


async def test_teamspace_view_visible_to_members_only(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    setup = await _setup_team_with_two_projects(client, owner, org["id"])
    member = await register_and_login(client)
    nonmember = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    await add_org_member(client, owner["headers"], org["id"], nonmember, role="member")
    member_id = await _me(client, member)
    await client.post(
        f"{API}/orgs/{org['id']}/teams/{setup['team']['id']}/members",
        json={"user_id": member_id},
        headers=owner["headers"],
    )

    view = (
        await client.post(
            f"{API}/orgs/{org['id']}/views",
            json={"name": "Team only", "scope": "teamspace", "team_id": setup["team"]["id"]},
            headers=owner["headers"],
        )
    ).json()["data"]

    member_list = await client.get(f"{API}/orgs/{org['id']}/views", headers=member["headers"])
    assert view["id"] in {v["id"] for v in member_list.json()["data"]}
    non_list = await client.get(f"{API}/orgs/{org['id']}/views", headers=nonmember["headers"])
    assert view["id"] not in {v["id"] for v in non_list.json()["data"]}
    denied = await client.get(
        f"{API}/orgs/{org['id']}/views/{view['id']}/tasks", headers=nonmember["headers"]
    )
    assert denied.status_code == 404, denied.text


async def test_org_team_view_scope_preserved(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    view = (
        await client.post(
            f"{API}/orgs/{org['id']}/views",
            json={"name": "Org wide", "scope": "team"},
            headers=owner["headers"],
        )
    ).json()["data"]
    assert view["scope"] == "team"
    assert view["team_id"] is None
