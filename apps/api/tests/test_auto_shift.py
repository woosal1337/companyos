"""Auto-shift dependent items on date change (COS-126)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_auto_shift_cascade(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="SHF")
    a = await create_task(client, h, org["id"], project["id"], title="A")
    b = await create_task(client, h, org["id"], project["id"], title="B")
    c = await create_task(client, h, org["id"], project["id"], title="C")

    async def dates(tid: str, start: str, due: str) -> None:
        await client.patch(
            f"{API}/orgs/{org['id']}/tasks/{tid}",
            json={"start_date": start, "due_date": due},
            headers=h,
        )

    await dates(a["id"], "2026-07-01", "2026-07-10")
    await dates(b["id"], "2026-07-11", "2026-07-15")
    await dates(c["id"], "2026-07-16", "2026-07-20")

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

    await dates(a["id"], "2026-07-01", "2026-07-20")
    shifted = await client.post(f"{API}/orgs/{org['id']}/tasks/{a['id']}/auto-shift", headers=h)
    assert shifted.status_code == 200, shifted.text
    moved = {s["title"]: s for s in shifted.json()["data"]["shifted"]}
    assert "B" in moved
    assert "C" in moved
    assert moved["B"]["start_date"] == "2026-07-21"
    assert moved["B"]["due_date"] == "2026-07-25"
    assert moved["C"]["start_date"] == "2026-07-26"
