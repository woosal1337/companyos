"""Publish a project as a public board with per-attribute privacy (COS-249)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_publish_board_attribute_privacy(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="PUB")
    await create_task(client, h, org["id"], project["id"], title="Visible task")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/publish-board"

    published = await client.post(base, json={"attributes": ["priority"]}, headers=h)
    assert published.status_code == 200, published.text
    token = published.json()["data"]["public_token"]
    assert published.json()["data"]["attributes"] == ["priority"]

    board = await client.get(f"{API}/public/boards/{token}")
    assert board.status_code == 200, board.text
    data = board.json()["data"]
    assert data["name"] and data["key"] == "PUB"
    all_tasks = [t for col in data["columns"] for t in col["tasks"]]
    visible = next(t for t in all_tasks if t["title"] == "Visible task")
    assert "priority" in visible
    assert "due_date" not in visible
    assert "has_assignee" not in visible

    upd = await client.patch(base, json={"attributes": ["priority", "due_date"]}, headers=h)
    assert set(upd.json()["data"]["attributes"]) == {"priority", "due_date"}
    board2 = await client.get(f"{API}/public/boards/{token}")
    t2 = next(t for col in board2.json()["data"]["columns"] for t in col["tasks"])
    assert "due_date" in t2

    await client.delete(base, headers=h)
    assert (await client.get(f"{API}/public/boards/{token}")).status_code == 404
