"""list_tasks module_id / cycle_id filters (COS-73)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_list_tasks_filtered_by_module(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    module = await client.post(
        f"{pbase}/modules", json={"name": "Checkout"}, headers=auth["headers"]
    )
    assert module.status_code == 201, module.text
    module_id = module.json()["data"]["id"]

    in_module = await create_task(
        client, auth["headers"], org["id"], project["id"], title="In module"
    )
    await create_task(client, auth["headers"], org["id"], project["id"], title="Loose")
    await client.post(
        f"{pbase}/modules/{module_id}/tasks/{in_module['id']}", headers=auth["headers"]
    )

    filtered = await client.get(f"{pbase}/tasks?module_id={module_id}", headers=auth["headers"])
    assert filtered.status_code == 200, filtered.text
    titles = [t["title"] for t in filtered.json()["data"]["items"]]
    assert titles == ["In module"]

    everything = await client.get(f"{pbase}/tasks", headers=auth["headers"])
    assert {t["title"] for t in everything.json()["data"]["items"]} == {"In module", "Loose"}
