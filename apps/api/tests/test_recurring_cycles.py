"""Recurring cycle generation (COS-85)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_generate_recurring_cycles(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles"

    res = await client.post(
        f"{pbase}/generate",
        json={
            "base_title": "Sprint",
            "count": 3,
            "duration_weeks": 2,
            "cooldown_days": 1,
            "start_date": "2026-07-06",
        },
        headers=h,
    )
    assert res.status_code == 201, res.text
    cycles = res.json()["data"]
    assert [c["name"] for c in cycles] == ["Sprint 1", "Sprint 2", "Sprint 3"]
    assert cycles[0]["start_date"] == "2026-07-06"
    assert cycles[0]["end_date"] == "2026-07-19"
    assert cycles[1]["start_date"] == "2026-07-21"

    listed = await client.get(pbase, headers=h)
    assert len(listed.json()["data"]) == 3
