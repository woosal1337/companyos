"""Runner scripts + cron + execution log (COS-251)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_runner_script_lifecycle(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    base = f"{API}/orgs/{org['id']}/runner/scripts"

    created = await client.post(
        base,
        json={
            "name": "Nightly digest",
            "language": "javascript",
            "code": "console.log('hi')",
            "cron_schedule": "0 9 * * 1",
        },
        headers=h,
    )
    assert created.status_code == 201, created.text
    sid = created.json()["data"]["id"]
    assert created.json()["data"]["cron_schedule"] == "0 9 * * 1"

    bad = await client.post(base, json={"name": "Bad", "cron_schedule": "not a cron"}, headers=h)
    assert bad.status_code == 400

    run = await client.post(f"{base}/{sid}/run", headers=h)
    assert run.status_code == 201, run.text
    assert run.json()["data"]["status"] == "queued"

    execs = await client.get(f"{base}/{sid}/executions", headers=h)
    assert len(execs.json()["data"]) == 1

    upd = await client.patch(f"{base}/{sid}", json={"enabled": True}, headers=h)
    assert upd.json()["data"]["enabled"] is True
    assert (await client.delete(f"{base}/{sid}", headers=h)).status_code == 200
