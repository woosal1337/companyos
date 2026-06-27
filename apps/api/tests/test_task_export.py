"""Project task export — CSV + JSON with filters (COS-271)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_task_export_csv_and_json(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="EXP")
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    done = await create_task(client, auth["headers"], org["id"], project["id"], title="Done one")
    await create_task(client, auth["headers"], org["id"], project["id"], title="Backlog one")
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{done['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )

    csv_export = await client.get(f"{pbase}/tasks/export.csv", headers=auth["headers"])
    assert csv_export.status_code == 200, csv_export.text
    assert csv_export.headers["content-type"].startswith("text/csv")
    body = csv_export.text
    assert "identifier,title,status,priority,kind,assignee_id,due_date,labels" in body
    assert "EXP-1" in body
    assert "Done one" in body
    assert "Backlog one" in body

    json_export = await client.get(f"{pbase}/tasks/export.json", headers=auth["headers"])
    assert json_export.status_code == 200
    titles = {t["title"] for t in json_export.json()["data"]}
    assert titles == {"Done one", "Backlog one"}

    filtered = await client.get(f"{pbase}/tasks/export.json?status=done", headers=auth["headers"])
    assert [t["title"] for t in filtered.json()["data"]] == ["Done one"]
