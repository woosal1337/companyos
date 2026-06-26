"""Saveable named task views (BT-05)."""

from httpx import AsyncClient

from tests.helpers import API, add_org_member, create_org, register_and_login


def _views(org_id: str) -> str:
    return f"{API}/orgs/{org_id}/views"


async def test_personal_view_crud_and_default_exclusivity(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    config = {"filters": {"status": "in_progress"}, "group_by": "assignee"}
    created = await client.post(
        _views(org["id"]),
        json={"name": "My active", "config": config, "scope": "personal", "is_default": True},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    first = created.json()["data"]
    assert first["scope"] == "personal"
    assert first["config"] == config
    assert first["is_default"] is True

    second = await client.post(
        _views(org["id"]),
        json={"name": "Backlog", "config": {}, "scope": "personal", "is_default": True},
        headers=auth["headers"],
    )
    second_id = second.json()["data"]["id"]

    listing = (await client.get(_views(org["id"]), headers=auth["headers"])).json()["data"]
    defaults = [v["id"] for v in listing if v["is_default"]]
    assert defaults == [second_id]

    await client.patch(
        f"{_views(org['id'])}/{first['id']}", json={"name": "Renamed"}, headers=auth["headers"]
    )
    deleted = await client.delete(f"{_views(org['id'])}/{first['id']}", headers=auth["headers"])
    assert deleted.status_code == 200, deleted.text


async def test_team_view_requires_admin_and_is_shared(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")

    blocked = await client.post(
        _views(org["id"]),
        json={"name": "Team board", "config": {}, "scope": "team"},
        headers=member["headers"],
    )
    assert blocked.status_code == 403, blocked.text

    created = await client.post(
        _views(org["id"]),
        json={"name": "Team board", "config": {}, "scope": "team"},
        headers=owner["headers"],
    )
    assert created.status_code == 201, created.text

    member_list = (await client.get(_views(org["id"]), headers=member["headers"])).json()["data"]
    assert [v["name"] for v in member_list] == ["Team board"]
    assert member_list[0]["scope"] == "team"


async def test_personal_views_are_private(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    await client.post(
        _views(org["id"]),
        json={"name": "Owner private", "config": {}, "scope": "personal"},
        headers=owner["headers"],
    )
    member_list = (await client.get(_views(org["id"]), headers=member["headers"])).json()["data"]
    assert member_list == []
