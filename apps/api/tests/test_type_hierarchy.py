"""Work-item type hierarchy / level builder (COS-71)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_type_levels_seed_and_nesting_enforcement(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    base = f"{API}/orgs/{org['id']}"

    levels = await client.get(f"{base}/work-item-type-levels", headers=auth["headers"])
    assert levels.status_code == 200, levels.text
    by_kind = {row["kind"]: row["level"] for row in levels.json()["data"]}
    assert by_kind["epic"] > by_kind["task"]

    epic = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Epic", kind="epic"
    )
    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Task")

    ok_child = await client.post(
        f"{base}/projects/{project['id']}/tasks",
        json={"title": "Child task", "parent_task_id": task["id"]},
        headers=auth["headers"],
    )
    assert ok_child.status_code == 201, ok_child.text

    bad = await client.post(
        f"{base}/projects/{project['id']}/tasks",
        json={"title": "Nested epic", "kind": "epic", "parent_task_id": task["id"]},
        headers=auth["headers"],
    )
    assert bad.status_code == 400, bad.text

    good = await client.post(
        f"{base}/projects/{project['id']}/tasks",
        json={"title": "Task under epic", "parent_task_id": epic["id"]},
        headers=auth["headers"],
    )
    assert good.status_code == 201, good.text


async def test_set_type_levels(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    base = f"{API}/orgs/{org['id']}/work-item-type-levels"
    await client.get(base, headers=auth["headers"])

    updated = await client.put(
        base,
        json={"levels": [{"kind": "bug", "level": 5}]},
        headers=auth["headers"],
    )
    assert updated.status_code == 200, updated.text
    by_kind = {row["kind"]: row["level"] for row in updated.json()["data"]}
    assert by_kind["bug"] == 5
