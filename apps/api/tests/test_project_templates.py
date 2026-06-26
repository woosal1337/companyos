"""Project templates: save-as-template + instantiate (COS-236)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_save_and_instantiate_project_template(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    source = await create_project(client, auth["headers"], org["id"], key="SRC")

    await client.patch(
        f"{API}/orgs/{org['id']}/projects/{source['id']}",
        json={
            "labels": ["Internal", "Q3"],
            "estimate_scale": ["1", "2", "3", "5"],
            "features": {"cycles": False},
        },
        headers=auth["headers"],
    )
    await create_task(client, auth["headers"], org["id"], source["id"], title="Set up CI")
    await create_task(client, auth["headers"], org["id"], source["id"], title="Write docs")

    saved = await client.post(
        f"{API}/orgs/{org['id']}/project-templates/from-project/{source['id']}",
        json={"name": "Service starter", "description": "Backend service preset"},
        headers=auth["headers"],
    )
    assert saved.status_code == 201, saved.text
    template = saved.json()["data"]
    assert template["config"]["labels"] == ["Internal", "Q3"]
    assert {item["title"] for item in template["config"]["seed_items"]} == {
        "Set up CI",
        "Write docs",
    }

    listing = await client.get(f"{API}/orgs/{org['id']}/project-templates", headers=auth["headers"])
    assert template["id"] in {t["id"] for t in listing.json()["data"]}

    created = await client.post(
        f"{API}/orgs/{org['id']}/project-templates/{template['id']}/instantiate",
        json={"name": "Payments", "key": "PAY"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    new_project = created.json()["data"]
    assert new_project["key"] == "PAY"
    assert new_project["labels"] == ["Internal", "Q3"]
    assert new_project["estimate_scale"] == ["1", "2", "3", "5"]
    assert new_project["features"] == {"cycles": False}

    tasks = await client.get(
        f"{API}/orgs/{org['id']}/projects/{new_project['id']}/tasks", headers=auth["headers"]
    )
    titles = {t["title"] for t in tasks.json()["data"]["items"]}
    assert {"Set up CI", "Write docs"} <= titles


async def test_template_name_conflict_and_delete(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="TPL")
    base = f"{API}/orgs/{org['id']}/project-templates"

    first = await client.post(
        f"{base}/from-project/{project['id']}", json={"name": "Dupe"}, headers=auth["headers"]
    )
    assert first.status_code == 201
    dupe = await client.post(
        f"{base}/from-project/{project['id']}", json={"name": "Dupe"}, headers=auth["headers"]
    )
    assert dupe.status_code == 409

    deleted = await client.delete(f"{base}/{first.json()['data']['id']}", headers=auth["headers"])
    assert deleted.status_code == 200
    assert (await client.get(base, headers=auth["headers"])).json()["data"] == []
