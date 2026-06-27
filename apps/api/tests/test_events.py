"""Calendar event scope, visibility, tenancy, and permission tests."""

from datetime import UTC, datetime, timedelta

from httpx import AsyncClient

from tests.helpers import API, add_org_member, create_org, register_and_login

WINDOW_FROM = datetime(2026, 1, 1, tzinfo=UTC).isoformat()
WINDOW_TO = datetime(2026, 12, 31, tzinfo=UTC).isoformat()


def _event_body(title: str, visibility: str = "team", **extra: object) -> dict[str, object]:
    start = datetime(2026, 6, 1, 9, 0, tzinfo=UTC)
    return {
        "title": title,
        "starts_at": start.isoformat(),
        "ends_at": (start + timedelta(hours=1)).isoformat(),
        "visibility": visibility,
        **extra,
    }


async def _create_event(
    client: AsyncClient, headers: dict[str, str], org_id: str, title: str, visibility: str = "team"
) -> dict[str, object]:
    response = await client.post(
        f"{API}/orgs/{org_id}/events",
        json=_event_body(title, visibility),
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return response.json()["data"]


async def _list_events(
    client: AsyncClient, headers: dict[str, str], org_id: str, scope: str = "all"
) -> list[dict[str, object]]:
    response = await client.get(
        f"{API}/orgs/{org_id}/events",
        params={"from": WINDOW_FROM, "to": WINDOW_TO, "scope": scope},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()["data"]


async def test_create_team_and_personal_event(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    team = await _create_event(client, auth["headers"], org["id"], "Team standup", "team")
    personal = await _create_event(client, auth["headers"], org["id"], "Dentist", "personal")
    assert team["scope"] == "team"
    assert team["owner_id"] is None
    assert personal["scope"] == "personal"
    assert personal["owner_id"] == auth["user_id"]


async def test_list_returns_team_and_own_personal_not_others(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member)

    team = await _create_event(client, owner["headers"], org["id"], "All hands", "team")
    owner_personal = await _create_event(
        client, owner["headers"], org["id"], "Owner private", "personal"
    )
    member_personal = await _create_event(
        client, member["headers"], org["id"], "Member private", "personal"
    )

    member_view = {item["id"] for item in await _list_events(client, member["headers"], org["id"])}
    assert team["id"] in member_view
    assert member_personal["id"] in member_view
    assert owner_personal["id"] not in member_view

    team_only = await _list_events(client, member["headers"], org["id"], scope="team")
    assert [item["id"] for item in team_only] == [team["id"]]

    personal_only = await _list_events(client, member["headers"], org["id"], scope="personal")
    assert [item["id"] for item in personal_only] == [member_personal["id"]]


async def test_other_user_personal_event_is_not_readable(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member)
    owner_personal = await _create_event(
        client, owner["headers"], org["id"], "Owner private", "personal"
    )
    response = await client.get(
        f"{API}/orgs/{org['id']}/events/{owner_personal['id']}", headers=member["headers"]
    )
    assert response.status_code == 404


async def test_tenant_isolation(client: AsyncClient) -> None:
    first = await register_and_login(client)
    second = await register_and_login(client)
    org_a = await create_org(client, first["headers"], name="Org A")
    org_b = await create_org(client, second["headers"], name="Org B")
    event = await _create_event(client, first["headers"], org_a["id"], "Private to A", "team")

    cross_org_list = await client.get(
        f"{API}/orgs/{org_b['id']}/events",
        params={"from": WINDOW_FROM, "to": WINDOW_TO},
        headers=second["headers"],
    )
    assert cross_org_list.status_code == 200
    assert cross_org_list.json()["data"] == []

    cross_org_get = await client.get(
        f"{API}/orgs/{org_a['id']}/events/{event['id']}", headers=second["headers"]
    )
    assert cross_org_get.status_code == 404


async def test_personal_event_only_owner_can_mutate(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member)
    personal = await _create_event(client, owner["headers"], org["id"], "Owner only", "personal")

    forbidden_update = await client.patch(
        f"{API}/orgs/{org['id']}/events/{personal['id']}",
        json={"title": "Hijacked"},
        headers=member["headers"],
    )
    assert forbidden_update.status_code == 404

    owner_update = await client.patch(
        f"{API}/orgs/{org['id']}/events/{personal['id']}",
        json={"title": "Renamed"},
        headers=owner["headers"],
    )
    assert owner_update.status_code == 200
    assert owner_update.json()["data"]["title"] == "Renamed"

    forbidden_delete = await client.delete(
        f"{API}/orgs/{org['id']}/events/{personal['id']}", headers=member["headers"]
    )
    assert forbidden_delete.status_code == 404


async def test_team_event_editable_by_creator(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    team = await _create_event(client, owner["headers"], org["id"], "Shared", "team")

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/events/{team['id']}",
        json={"location": "Room 4"},
        headers=owner["headers"],
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["location"] == "Room 4"

    deleted = await client.delete(
        f"{API}/orgs/{org['id']}/events/{team['id']}", headers=owner["headers"]
    )
    assert deleted.status_code == 200


async def test_team_event_not_editable_by_other_member(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    creator = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], creator)
    await add_org_member(client, owner["headers"], org["id"], member)
    team = await _create_event(client, creator["headers"], org["id"], "Shared", "team")

    forbidden_update = await client.patch(
        f"{API}/orgs/{org['id']}/events/{team['id']}",
        json={"location": "Room 4"},
        headers=member["headers"],
    )
    assert forbidden_update.status_code == 403
    assert "creator or an admin" in forbidden_update.json()["message"]

    forbidden_delete = await client.delete(
        f"{API}/orgs/{org['id']}/events/{team['id']}", headers=member["headers"]
    )
    assert forbidden_delete.status_code == 403


async def test_team_event_editable_by_admin(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    creator = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], creator)
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    team = await _create_event(client, creator["headers"], org["id"], "Shared", "team")

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/events/{team['id']}",
        json={"location": "Boardroom"},
        headers=admin["headers"],
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["location"] == "Boardroom"


async def test_visibility_flip_changes_scope(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    team = await _create_event(client, auth["headers"], org["id"], "Flip me", "team")
    flipped = await client.patch(
        f"{API}/orgs/{org['id']}/events/{team['id']}",
        json={"visibility": "personal"},
        headers=auth["headers"],
    )
    assert flipped.status_code == 200
    assert flipped.json()["data"]["scope"] == "personal"
    assert flipped.json()["data"]["owner_id"] == auth["user_id"]


async def test_visibility_flip_forbidden_for_non_creator_member(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    creator = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], creator)
    await add_org_member(client, owner["headers"], org["id"], member)
    team = await _create_event(client, creator["headers"], org["id"], "Shared", "team")

    response = await client.patch(
        f"{API}/orgs/{org['id']}/events/{team['id']}",
        json={"visibility": "personal"},
        headers=member["headers"],
    )
    assert response.status_code == 403

    still_team = await client.get(
        f"{API}/orgs/{org['id']}/events/{team['id']}", headers=member["headers"]
    )
    assert still_team.status_code == 200
    assert still_team.json()["data"]["scope"] == "team"


async def test_admin_flip_assigns_creator_not_actor(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    creator = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], creator)
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    team = await _create_event(client, creator["headers"], org["id"], "Shared", "team")

    flipped = await client.patch(
        f"{API}/orgs/{org['id']}/events/{team['id']}",
        json={"visibility": "personal"},
        headers=admin["headers"],
    )
    assert flipped.status_code == 200
    assert flipped.json()["data"]["scope"] == "personal"
    assert flipped.json()["data"]["owner_id"] == creator["user_id"]

    creator_view = await client.get(
        f"{API}/orgs/{org['id']}/events/{team['id']}", headers=creator["headers"]
    )
    assert creator_view.status_code == 200
    admin_view = await client.get(
        f"{API}/orgs/{org['id']}/events/{team['id']}", headers=admin["headers"]
    )
    assert admin_view.status_code == 404


async def test_list_range_coerces_naive_datetimes_to_utc(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    start = datetime(2026, 6, 1, 9, 0, tzinfo=UTC)
    created = await client.post(
        f"{API}/orgs/{org['id']}/events",
        json={
            "title": "TZ check",
            "starts_at": start.isoformat(),
            "ends_at": (start + timedelta(hours=1)).isoformat(),
        },
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    event_id = created.json()["data"]["id"]

    naive_in = await client.get(
        f"{API}/orgs/{org['id']}/events",
        params={"from": "2026-06-01T08:00:00", "to": "2026-06-01T11:00:00"},
        headers=auth["headers"],
    )
    assert naive_in.status_code == 200, naive_in.text
    assert event_id in {item["id"] for item in naive_in.json()["data"]}

    naive_out = await client.get(
        f"{API}/orgs/{org['id']}/events",
        params={"from": "2026-06-01T11:00:00", "to": "2026-06-01T12:00:00"},
        headers=auth["headers"],
    )
    assert naive_out.status_code == 200, naive_out.text
    assert event_id not in {item["id"] for item in naive_out.json()["data"]}


async def test_naive_create_datetimes_stored_as_utc(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    created = await client.post(
        f"{API}/orgs/{org['id']}/events",
        json={
            "title": "Naive write",
            "starts_at": "2026-06-02T09:00:00",
            "ends_at": "2026-06-02T10:00:00",
        },
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    event_id = created.json()["data"]["id"]

    aware_window = await client.get(
        f"{API}/orgs/{org['id']}/events",
        params={
            "from": datetime(2026, 6, 2, 8, 0, tzinfo=UTC).isoformat(),
            "to": datetime(2026, 6, 2, 11, 0, tzinfo=UTC).isoformat(),
        },
        headers=auth["headers"],
    )
    assert aware_window.status_code == 200, aware_window.text
    assert event_id in {item["id"] for item in aware_window.json()["data"]}


async def test_list_excludes_events_outside_window(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    far_start = datetime(2030, 1, 1, 9, 0, tzinfo=UTC)
    response = await client.post(
        f"{API}/orgs/{org['id']}/events",
        json={
            "title": "Way out",
            "starts_at": far_start.isoformat(),
            "ends_at": (far_start + timedelta(hours=1)).isoformat(),
        },
        headers=auth["headers"],
    )
    assert response.status_code == 201
    in_window = await _list_events(client, auth["headers"], org["id"])
    assert in_window == []
