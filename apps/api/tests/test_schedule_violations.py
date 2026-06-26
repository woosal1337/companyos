"""Red-line scheduling violations on the timeline (COS-138)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_violation_flagged(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="VIO")
    a = await create_task(client, h, org["id"], project["id"], title="Pred")
    b = await create_task(client, h, org["id"], project["id"], title="Succ")

    async def dates(tid: str, start: str, due: str) -> None:
        await client.patch(
            f"{API}/orgs/{org['id']}/tasks/{tid}",
            json={"start_date": start, "due_date": due},
            headers=h,
        )

    await dates(a["id"], "2026-07-10", "2026-07-20")
    await dates(b["id"], "2026-07-12", "2026-07-18")
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{b['id']}/schedule-links",
        json={
            "other_task_id": a["id"],
            "dependency_type": "finish_to_start",
            "other_is_predecessor": True,
        },
        headers=h,
    )

    tl = (
        await client.get(f"{API}/orgs/{org['id']}/projects/{project['id']}/timeline", headers=h)
    ).json()["data"]
    assert tl["violation_count"] == 1
    assert tl["links"][0]["violated"] is True
    by_id = {t["id"]: t for t in tl["tasks"]}
    assert by_id[b["id"]]["is_violated"] is True
    assert by_id[a["id"]]["is_violated"] is False

    await dates(b["id"], "2026-07-21", "2026-07-25")
    tl2 = (
        await client.get(f"{API}/orgs/{org['id']}/projects/{project['id']}/timeline", headers=h)
    ).json()["data"]
    assert tl2["violation_count"] == 0
