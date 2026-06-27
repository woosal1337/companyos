"""Internal/external comment visibility (COS-92)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    create_task,
    register_and_login,
)


async def test_comment_visibility_filters_guests(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    project = await create_project(client, owner["headers"], org["id"])
    task = await create_task(client, owner["headers"], org["id"], project["id"])
    base = f"{API}/orgs/{org['id']}/comments"

    internal = await client.post(
        base,
        json={"entity_type": "task", "entity_id": task["id"], "content": "team only"},
        headers=owner["headers"],
    )
    assert internal.json()["data"]["visibility"] == "internal"

    await client.post(
        base,
        json={
            "entity_type": "task",
            "entity_id": task["id"],
            "content": "for the customer",
            "visibility": "external",
        },
        headers=owner["headers"],
    )

    owner_list = await client.get(
        f"{base}?entity_type=task&entity_id={task['id']}", headers=owner["headers"]
    )
    assert len(owner_list.json()["data"]["items"]) == 2

    guest = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], guest, role="guest")
    guest_list = await client.get(
        f"{base}?entity_type=task&entity_id={task['id']}", headers=guest["headers"]
    )
    items = guest_list.json()["data"]["items"]
    assert [c["content"] for c in items] == ["for the customer"]
    assert all(c["visibility"] == "external" for c in items)


async def test_comment_anchor_roundtrip(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    note = (
        await client.post(
            f"{API}/orgs/{org['id']}/notes",
            json={"title": "Doc", "content": "Some anchored text here."},
            headers=auth["headers"],
        )
    ).json()["data"]
    created = await client.post(
        f"{API}/orgs/{org['id']}/comments",
        json={
            "entity_type": "note",
            "entity_id": note["id"],
            "content": "needs a rewrite",
            "anchor": "anchored text",
        },
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    assert created.json()["data"]["anchor"] == "anchored text"
