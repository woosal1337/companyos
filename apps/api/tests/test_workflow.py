"""Per-team workflow statuses: seeding, CRUD, scope, and admin gating (BT-09)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    create_task,
    register_and_login,
)


def _wf(org_id: str) -> str:
    return f"{API}/orgs/{org_id}/workflow/statuses"


async def test_org_creation_seeds_default_workflow(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    response = await client.get(_wf(org["id"]), headers=auth["headers"])
    assert response.status_code == 200, response.text
    statuses = response.json()["data"]
    assert [s["name"] for s in statuses] == [
        "Backlog",
        "Todo",
        "In Progress",
        "In Review",
        "Done",
        "Cancelled",
    ]
    by_name = {s["name"]: s for s in statuses}
    assert by_name["Backlog"]["category"] == "backlog"
    assert by_name["Todo"]["category"] == "unstarted"
    assert by_name["In Progress"]["category"] == "started"
    assert by_name["In Review"]["category"] == "started"
    assert by_name["Done"]["category"] == "completed"
    assert by_name["Cancelled"]["category"] == "cancelled"
    assert by_name["Backlog"]["is_default"] is True
    assert sum(1 for s in statuses if s["is_default"]) == 1


async def test_task_carries_workflow_status_id(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="WFW")

    statuses = (await client.get(_wf(org["id"]), headers=auth["headers"])).json()["data"]
    by_name = {s["name"]: s["id"] for s in statuses}

    task = await create_task(client, auth["headers"], org["id"], project["id"])
    assert task["workflow_status_id"] == by_name["Backlog"]

    moved = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "in_progress"},
        headers=auth["headers"],
    )
    assert moved.status_code == 200, moved.text
    assert moved.json()["data"]["workflow_status_id"] == by_name["In Progress"]


async def test_role_gated_transition(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    project = await create_project(client, owner["headers"], org["id"], key="GAT")
    statuses = (await client.get(_wf(org["id"]), headers=owner["headers"])).json()["data"]
    by_name = {s["name"]: s["id"] for s in statuses}

    created = await client.post(
        f"{API}/orgs/{org['id']}/workflow/transitions",
        json={
            "from_status_id": by_name["Backlog"],
            "to_status_id": by_name["Todo"],
            "required_role": "admin",
        },
        headers=owner["headers"],
    )
    assert created.status_code == 201, created.text
    assert created.json()["data"]["required_role"] == "admin"

    task = await create_task(client, owner["headers"], org["id"], project["id"])

    viewer = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], viewer, role="member")
    viewer_me = (await client.get(f"{API}/users/me", headers=viewer["headers"])).json()["data"]
    await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members",
        json={"user_id": viewer_me["id"], "role": "viewer"},
        headers=owner["headers"],
    )
    blocked = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "todo"},
        headers=viewer["headers"],
    )
    assert blocked.status_code == 403, blocked.text

    allowed = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "todo"},
        headers=owner["headers"],
    )
    assert allowed.status_code == 200, allowed.text


async def test_two_step_status_deletion_with_transfer(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="DEL")
    statuses = (await client.get(_wf(org["id"]), headers=auth["headers"])).json()["data"]
    by_name = {s["name"]: s["id"] for s in statuses}

    task = await create_task(client, auth["headers"], org["id"], project["id"])

    no_transfer = await client.delete(
        f"{API}/orgs/{org['id']}/workflow/statuses/{by_name['Backlog']}", headers=auth["headers"]
    )
    assert no_transfer.status_code == 409, no_transfer.text

    moved = await client.delete(
        f"{API}/orgs/{org['id']}/workflow/statuses/{by_name['Backlog']}?transfer_to={by_name['Todo']}",
        headers=auth["headers"],
    )
    assert moved.status_code == 200, moved.text

    fetched = await client.get(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}", headers=auth["headers"]
    )
    data = fetched.json()["data"]
    assert data["status"] == "todo"
    assert data["workflow_status_id"] == by_name["Todo"]


async def test_entry_state_allow_new_items(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="ENT")
    statuses = (await client.get(_wf(org["id"]), headers=auth["headers"])).json()["data"]
    done = next(s for s in statuses if s["name"] == "Done")
    assert done["allow_new_items"] is True

    await client.patch(
        f"{API}/orgs/{org['id']}/workflow/statuses/{done['id']}",
        json={"allow_new_items": False},
        headers=auth["headers"],
    )

    blocked = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/tasks",
        json={"title": "Born done", "status": "done"},
        headers=auth["headers"],
    )
    assert blocked.status_code == 400, blocked.text

    ok_create = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/tasks",
        json={"title": "Normal"},
        headers=auth["headers"],
    )
    assert ok_create.status_code == 201, ok_create.text


async def test_no_backward_regression_comment_and_block(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="REG")
    task = await create_task(client, auth["headers"], org["id"], project["id"])

    async def move(status: str) -> int:
        r = await client.post(
            f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
            json={"status": status},
            headers=auth["headers"],
        )
        return r.status_code

    assert await move("in_progress") == 200
    assert await move("todo") == 200
    comments = await client.get(
        f"{API}/orgs/{org['id']}/comments",
        params={"entity_type": "task", "entity_id": task["id"]},
        headers=auth["headers"],
    )
    bodies = [c["content"] for c in comments.json()["data"]["items"]]
    assert any("moved back" in body.lower() for body in bodies)

    await client.patch(
        f"{API}/orgs/{org['id']}",
        json={"block_backward_transitions": True},
        headers=auth["headers"],
    )
    assert await move("in_progress") == 200
    assert await move("backlog") == 403


async def test_transition_guardrails_enforced(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="GRD")
    statuses = (await client.get(_wf(org["id"]), headers=auth["headers"])).json()["data"]
    by_name = {s["name"]: s["id"] for s in statuses}

    task = await create_task(client, auth["headers"], org["id"], project["id"])

    allow = await client.post(
        f"{API}/orgs/{org['id']}/workflow/transitions",
        json={"from_status_id": by_name["Backlog"], "to_status_id": by_name["Todo"]},
        headers=auth["headers"],
    )
    assert allow.status_code == 201, allow.text

    blocked = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "in_progress"},
        headers=auth["headers"],
    )
    assert blocked.status_code == 403, blocked.text

    ok_move = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "todo"},
        headers=auth["headers"],
    )
    assert ok_move.status_code == 200, ok_move.text
    open_move = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{task['id']}/status",
        json={"status": "in_progress"},
        headers=auth["headers"],
    )
    assert open_move.status_code == 200, open_move.text


async def test_admin_can_add_status_within_a_category(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    response = await client.post(
        _wf(org["id"]),
        json={"name": "In QA", "category": "started", "color": "info"},
        headers=auth["headers"],
    )
    assert response.status_code == 201, response.text
    created = response.json()["data"]
    assert created["name"] == "In QA"
    assert created["category"] == "started"
    assert created["color"] == "info"
    assert created["team_id"] is None
    listing = await client.get(_wf(org["id"]), headers=auth["headers"])
    assert any(s["name"] == "In QA" for s in listing.json()["data"])


async def test_duplicate_name_in_scope_conflicts(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    body = {"name": "In QA", "category": "started"}
    first = await client.post(_wf(org["id"]), json=body, headers=auth["headers"])
    assert first.status_code == 201, first.text
    second = await client.post(_wf(org["id"]), json=body, headers=auth["headers"])
    assert second.status_code == 409, second.text


async def test_non_admin_cannot_mutate_but_can_read(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    blocked = await client.post(
        _wf(org["id"]),
        json={"name": "Blocked", "category": "started"},
        headers=member["headers"],
    )
    assert blocked.status_code == 403, blocked.text
    readable = await client.get(_wf(org["id"]), headers=member["headers"])
    assert readable.status_code == 200


async def test_make_default_is_exclusive_within_scope(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    added = await client.post(
        _wf(org["id"]),
        json={"name": "Triaged", "category": "backlog"},
        headers=auth["headers"],
    )
    new_id = added.json()["data"]["id"]
    patched = await client.patch(
        f"{_wf(org['id'])}/{new_id}", json={"is_default": True}, headers=auth["headers"]
    )
    assert patched.status_code == 200, patched.text
    statuses = (await client.get(_wf(org["id"]), headers=auth["headers"])).json()["data"]
    defaults = [s for s in statuses if s["is_default"]]
    assert len(defaults) == 1
    assert defaults[0]["id"] == new_id


async def test_rename_recolor_and_delete(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    added = await client.post(
        _wf(org["id"]), json={"name": "In QA", "category": "started"}, headers=auth["headers"]
    )
    status_id = added.json()["data"]["id"]
    renamed = await client.patch(
        f"{_wf(org['id'])}/{status_id}",
        json={"name": "In Review 2", "color": "teal"},
        headers=auth["headers"],
    )
    assert renamed.json()["data"]["name"] == "In Review 2"
    assert renamed.json()["data"]["color"] == "teal"
    deleted = await client.delete(f"{_wf(org['id'])}/{status_id}", headers=auth["headers"])
    assert deleted.status_code == 200, deleted.text
    listing = await client.get(_wf(org["id"]), headers=auth["headers"])
    assert all(s["id"] != status_id for s in listing.json()["data"])


async def test_team_scope_is_separate_from_org_scope(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    team_response = await client.post(
        f"{API}/orgs/{org['id']}/teams", json={"name": "Platform"}, headers=auth["headers"]
    )
    assert team_response.status_code == 201, team_response.text
    team_id = team_response.json()["data"]["id"]
    await client.post(
        _wf(org["id"]),
        json={"name": "In QA", "category": "started", "team_id": team_id},
        headers=auth["headers"],
    )
    team_list = await client.get(f"{_wf(org['id'])}?team_id={team_id}", headers=auth["headers"])
    assert [s["name"] for s in team_list.json()["data"]] == ["In QA"]
    org_list = await client.get(_wf(org["id"]), headers=auth["headers"])
    assert all(s["name"] != "In QA" for s in org_list.json()["data"])
    assert len(org_list.json()["data"]) == 6
