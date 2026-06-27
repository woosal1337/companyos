"""Convert a sticky into a task or note (COS-162)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_convert_sticky_to_task_and_note(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="STK")
    base = f"{API}/orgs/{org['id']}/stickies"

    s1 = await client.post(base, json={"content": "Ship the dock\nmore detail"}, headers=h)
    sid1 = s1.json()["data"]["id"]
    conv = await client.post(
        f"{base}/{sid1}/convert",
        json={"target": "task", "project_id": project["id"]},
        headers=h,
    )
    assert conv.status_code == 201, conv.text
    assert conv.json()["data"]["target"] == "task"
    task_id = conv.json()["data"]["entity_id"]
    task = await client.get(f"{API}/orgs/{org['id']}/tasks/{task_id}", headers=h)
    assert task.json()["data"]["title"] == "Ship the dock"
    assert all(s["id"] != sid1 for s in (await client.get(base, headers=h)).json()["data"])

    s2 = await client.post(base, json={"content": "A wiki idea"}, headers=h)
    sid2 = s2.json()["data"]["id"]
    conv2 = await client.post(
        f"{base}/{sid2}/convert", json={"target": "note", "delete_after": False}, headers=h
    )
    assert conv2.status_code == 201, conv2.text
    assert conv2.json()["data"]["target"] == "note"
    assert any(s["id"] == sid2 for s in (await client.get(base, headers=h)).json()["data"])

    s3 = await client.post(base, json={"content": "x"}, headers=h)
    bad = await client.post(
        f"{base}/{s3.json()['data']['id']}/convert", json={"target": "task"}, headers=h
    )
    assert bad.status_code == 400
