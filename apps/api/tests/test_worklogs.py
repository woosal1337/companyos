"""Worklog (time tracking) tests (COS-174)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_worklog_crud_and_totals(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="WRK")
    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Build")
    base = f"{API}/orgs/{org['id']}/tasks/{task['id']}/worklogs"

    first = await client.post(
        base,
        json={"minutes": 90, "note": "Pairing", "logged_at": "2026-06-18"},
        headers=auth["headers"],
    )
    assert first.status_code == 201, first.text
    assert first.json()["data"]["minutes"] == 90
    assert first.json()["data"]["user_name"]

    await client.post(base, json={"minutes": 30}, headers=auth["headers"])

    listing = await client.get(base, headers=auth["headers"])
    assert listing.status_code == 200, listing.text
    data = listing.json()["data"]
    assert len(data["entries"]) == 2
    assert data["total_minutes"] == 120

    summary = await client.get(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/worklogs/summary", headers=auth["headers"]
    )
    assert summary.json()["data"]["total_minutes"] == 120

    export = await client.get(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/worklogs/export.csv",
        headers=auth["headers"],
    )
    assert export.status_code == 200
    assert export.headers["content-type"].startswith("text/csv")
    body = export.text
    assert "logged_at,task,logged_by,minutes,note" in body
    assert "WRK-1" in body
    assert "Pairing" in body
    assert body.count("\n") == 3

    filtered = await client.get(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/worklogs/export.csv"
        "?start_date=2026-06-18&end_date=2026-06-18",
        headers=auth["headers"],
    )
    assert "Pairing" in filtered.text

    worklog_id = first.json()["data"]["id"]
    deleted = await client.delete(f"{base}/{worklog_id}", headers=auth["headers"])
    assert deleted.status_code == 200
    after = await client.get(base, headers=auth["headers"])
    assert after.json()["data"]["total_minutes"] == 30


async def test_worklog_minutes_validation(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="WRV")
    task = await create_task(client, auth["headers"], org["id"], project["id"])
    base = f"{API}/orgs/{org['id']}/tasks/{task['id']}/worklogs"

    assert (
        await client.post(base, json={"minutes": 0}, headers=auth["headers"])
    ).status_code == 422
    assert (
        await client.post(base, json={"minutes": -5}, headers=auth["headers"])
    ).status_code == 422
