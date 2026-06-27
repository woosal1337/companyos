"""Universal deep-link resolver (COS-226)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_resolve_task_project_comment(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="RES")
    task = await create_task(client, h, org["id"], project["id"], title="Resolve me")
    base = f"{API}/orgs/{org['id']}/resolve"

    ident = task["identifier"]
    r1 = await client.get(f"{base}/{ident}", headers=h)
    assert r1.status_code == 200, r1.text
    assert r1.json()["data"]["kind"] == "task"
    assert r1.json()["data"]["task_id"] == task["id"]
    assert r1.json()["data"]["project_id"] == project["id"]

    r2 = await client.get(f"{base}/{task['id']}", headers=h)
    assert r2.json()["data"]["kind"] == "task"

    r3 = await client.get(f"{base}/RES", headers=h)
    assert r3.json()["data"]["kind"] == "project"
    assert r3.json()["data"]["project_id"] == project["id"]

    c = await client.post(
        f"{API}/orgs/{org['id']}/comments",
        json={"entity_type": "task", "entity_id": task["id"], "content": "hi"},
        headers=h,
    )
    cid = c.json()["data"]["id"]
    r4 = await client.get(f"{base}/{cid}", headers=h)
    assert r4.json()["data"]["kind"] == "comment"
    assert r4.json()["data"]["comment_id"] == cid
    assert r4.json()["data"]["task_id"] == task["id"]
    assert r4.json()["data"]["entity_type"] == "task"

    assert (await client.get(f"{base}/NOPE-99", headers=h)).status_code == 404
