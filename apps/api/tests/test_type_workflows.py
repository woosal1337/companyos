"""Type-specific workflow transitions (COS-202)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_type_specific_transition_precedence(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    project = await create_project(client, owner["headers"], org["id"], key="TWF")
    statuses = (
        await client.get(f"{API}/orgs/{org['id']}/workflow/statuses", headers=owner["headers"])
    ).json()["data"]
    by_name = {s["name"]: s["id"] for s in statuses}

    created = await client.post(
        f"{API}/orgs/{org['id']}/workflow/transitions",
        json={
            "from_status_id": by_name["Backlog"],
            "to_status_id": by_name["Todo"],
            "kind": "bug",
        },
        headers=owner["headers"],
    )
    assert created.status_code == 201, created.text
    assert created.json()["data"]["kind"] == "bug"

    bug = await create_task(
        client, owner["headers"], org["id"], project["id"], kind="bug", severity="medium"
    )
    regular = await create_task(client, owner["headers"], org["id"], project["id"])

    blocked = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{bug['id']}/status",
        json={"status": "in_progress"},
        headers=owner["headers"],
    )
    assert blocked.status_code == 403, blocked.text

    allowed = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{bug['id']}/status",
        json={"status": "todo"},
        headers=owner["headers"],
    )
    assert allowed.status_code == 200, allowed.text

    regular_move = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{regular['id']}/status",
        json={"status": "in_progress"},
        headers=owner["headers"],
    )
    assert regular_move.status_code == 200, regular_move.text
