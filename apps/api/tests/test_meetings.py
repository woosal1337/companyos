"""Meeting CRUD, Folio import, and transcript paging tests."""

from datetime import UTC, datetime

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    import_meeting,
    register_and_login,
)


async def test_folio_import_persists_segments(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    meeting = await import_meeting(client, auth["headers"], org["id"], segment_count=4)
    assert meeting["source"] == "folio"
    assert meeting["external_attendees"] == ["External Guest"]

    segments = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}/segments", headers=auth["headers"]
    )
    assert segments.status_code == 200
    data = segments.json()["data"]
    assert data["total"] == 4
    assert [segment["position"] for segment in data["items"]] == [0, 1, 2, 3]
    assert data["items"][0]["text"] == "Segment text number 0"


async def test_segment_paging(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    meeting = await import_meeting(client, auth["headers"], org["id"], segment_count=7)
    page = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}/segments",
        params={"limit": 3, "offset": 3},
        headers=auth["headers"],
    )
    data = page.json()["data"]
    assert data["total"] == 7
    assert data["limit"] == 3
    assert [segment["position"] for segment in data["items"]] == [3, 4, 5]


async def test_meeting_manual_crud(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    created = await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "1:1",
            "started_at": datetime.now(UTC).isoformat(),
            "attendee_ids": [auth["user_id"]],
            "external_attendees": ["Guest"],
        },
        headers=auth["headers"],
    )
    assert created.status_code == 201
    meeting = created.json()["data"]
    assert meeting["source"] == "manual"

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}",
        json={"title": "Renamed 1:1"},
        headers=auth["headers"],
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["title"] == "Renamed 1:1"

    listing = await client.get(f"{API}/orgs/{org['id']}/meetings", headers=auth["headers"])
    assert listing.json()["data"]["total"] == 1

    deleted = await client.delete(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=auth["headers"]
    )
    assert deleted.status_code == 200
    gone = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=auth["headers"]
    )
    assert gone.status_code == 404


async def test_meeting_attendees_must_be_org_members(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    outsider = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    response = await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "Bad attendee",
            "started_at": datetime.now(UTC).isoformat(),
            "attendee_ids": [outsider["user_id"]],
        },
        headers=auth["headers"],
    )
    assert response.status_code == 400


async def test_plain_member_cannot_edit_or_delete_others_meeting(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    meeting = await import_meeting(client, owner["headers"], org["id"])

    edit = await client.patch(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}",
        json={"title": "Hijacked"},
        headers=member["headers"],
    )
    assert edit.status_code == 403

    delete = await client.delete(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=member["headers"]
    )
    assert delete.status_code == 403

    still_there = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=owner["headers"]
    )
    assert still_there.status_code == 200
    assert still_there.json()["data"]["title"] == "Weekly sync"


async def test_admin_can_edit_and_delete_any_meeting(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    admin = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], admin, role="admin")
    meeting = await import_meeting(client, owner["headers"], org["id"])

    edit = await client.patch(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}",
        json={"title": "Admin edit"},
        headers=admin["headers"],
    )
    assert edit.status_code == 200
    assert edit.json()["data"]["title"] == "Admin edit"

    delete = await client.delete(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=admin["headers"]
    )
    assert delete.status_code == 200


async def test_creator_can_edit_own_meeting(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    meeting = await import_meeting(client, member["headers"], org["id"])

    edit = await client.patch(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}",
        json={"title": "My own meeting"},
        headers=member["headers"],
    )
    assert edit.status_code == 200
    assert edit.json()["data"]["title"] == "My own meeting"


async def test_non_project_member_cannot_read_project_meeting(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    project = await create_project(client, owner["headers"], org["id"])
    created = await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "Project-scoped",
            "started_at": datetime.now(UTC).isoformat(),
            "project_id": project["id"],
        },
        headers=owner["headers"],
    )
    assert created.status_code == 201
    meeting = created.json()["data"]

    read = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=member["headers"]
    )
    assert read.status_code == 404

    segments = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}/segments", headers=member["headers"]
    )
    assert segments.status_code == 404


async def test_project_meeting_hidden_from_list_for_non_members(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    project = await create_project(client, owner["headers"], org["id"])
    await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "Project-scoped",
            "started_at": datetime.now(UTC).isoformat(),
            "project_id": project["id"],
        },
        headers=owner["headers"],
    )
    await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={"title": "Org-wide", "started_at": datetime.now(UTC).isoformat()},
        headers=owner["headers"],
    )

    listing = await client.get(f"{API}/orgs/{org['id']}/meetings", headers=member["headers"])
    data = listing.json()["data"]
    titles = {item["title"] for item in data["items"]}
    assert titles == {"Org-wide"}
    assert data["total"] == 1


async def test_project_member_can_read_project_meeting(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    project = await create_project(client, owner["headers"], org["id"])
    add = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members",
        json={"user_id": member["user_id"]},
        headers=owner["headers"],
    )
    assert add.status_code == 201
    created = await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "Shared",
            "started_at": datetime.now(UTC).isoformat(),
            "project_id": project["id"],
        },
        headers=owner["headers"],
    )
    meeting = created.json()["data"]

    read = await client.get(
        f"{API}/orgs/{org['id']}/meetings/{meeting['id']}", headers=member["headers"]
    )
    assert read.status_code == 200


async def test_member_cannot_attach_meeting_to_foreign_project(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    member = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    project = await create_project(client, owner["headers"], org["id"])

    response = await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "Sneaky attach",
            "started_at": datetime.now(UTC).isoformat(),
            "project_id": project["id"],
        },
        headers=member["headers"],
    )
    assert response.status_code == 403
