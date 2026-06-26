"""CSV work-item import (COS-270)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_csv_import_creates_tasks(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])

    csv_text = (
        "Summary,Description,Status,Priority,Type\n"
        "Set up CI,Configure pipelines,In Progress,High,Task\n"
        "Login crashes,NPE on submit,Open,Highest,Bug\n"
        ",missing title row,Done,Low,Task\n"
    )
    res = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/import",
        json={"content": csv_text},
        headers=h,
    )
    assert res.status_code == 201, res.text
    data = res.json()["data"]
    assert data["created_count"] == 2
    assert data["skipped_count"] == 1
    assert len(data["identifiers"]) == 2

    tasks = await client.get(f"{API}/orgs/{org['id']}/projects/{project['id']}/tasks", headers=h)
    rows = tasks.json()["data"]["items"]
    ci = next(t for t in rows if t["title"] == "Set up CI")
    assert ci["status"] == "in_progress"
    assert ci["priority"] == "high"
    bug = next(t for t in rows if t["title"] == "Login crashes")
    assert bug["kind"] == "bug"
    assert bug["priority"] == "urgent"
