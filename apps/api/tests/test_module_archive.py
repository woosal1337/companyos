"""Module archive/restore + CSV export (COS-58)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_module_archive_restore_and_export(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/modules"

    module = (await client.post(base, json={"name": "Billing"}, headers=auth["headers"])).json()[
        "data"
    ]
    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Invoices")
    await client.post(f"{base}/{module['id']}/tasks/{task['id']}", headers=auth["headers"])

    archived = await client.post(f"{base}/{module['id']}/archive", headers=auth["headers"])
    assert archived.status_code == 200, archived.text
    assert archived.json()["data"]["archived_at"] is not None
    assert (await client.get(base, headers=auth["headers"])).json()["data"] == []
    with_archived = await client.get(f"{base}?include_archived=true", headers=auth["headers"])
    assert len(with_archived.json()["data"]) == 1

    restored = await client.post(f"{base}/{module['id']}/restore", headers=auth["headers"])
    assert restored.json()["data"]["archived_at"] is None
    assert len((await client.get(base, headers=auth["headers"])).json()["data"]) == 1

    export = await client.get(f"{base}/{module['id']}/export.csv", headers=auth["headers"])
    assert export.status_code == 200
    assert export.headers["content-type"].startswith("text/csv")
    body = export.text
    assert "number,title,status,priority,kind,assignee_id" in body
    assert "Invoices" in body
