"""Project timeline + critical path (COS-115)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_timeline_and_critical_path(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="GAN")
    a = await create_task(client, h, org["id"], project["id"], title="Design")
    b = await create_task(client, h, org["id"], project["id"], title="Build")
    c = await create_task(client, h, org["id"], project["id"], title="Ship")
    side = await create_task(client, h, org["id"], project["id"], title="Docs")

    upd = await client.patch(
        f"{API}/orgs/{org['id']}/tasks/{a['id']}",
        json={"start_date": "2026-07-01", "due_date": "2026-07-05"},
        headers=h,
    )
    assert upd.json()["data"]["start_date"] == "2026-07-01"

    async def link(pred: str, succ: str) -> None:
        await client.post(
            f"{API}/orgs/{org['id']}/tasks/{succ}/schedule-links",
            json={
                "other_task_id": pred,
                "dependency_type": "finish_to_start",
                "other_is_predecessor": True,
            },
            headers=h,
        )

    await link(a["id"], b["id"])
    await link(b["id"], c["id"])

    tl = await client.get(f"{API}/orgs/{org['id']}/projects/{project['id']}/timeline", headers=h)
    assert tl.status_code == 200, tl.text
    data = tl.json()["data"]
    assert len(data["tasks"]) == 4
    assert len(data["links"]) == 2
    assert data["critical_path"] == [a["id"], b["id"], c["id"]]
    by_id = {t["id"]: t for t in data["tasks"]}
    assert by_id[a["id"]]["on_critical_path"] is True
    assert by_id[side["id"]]["on_critical_path"] is False
