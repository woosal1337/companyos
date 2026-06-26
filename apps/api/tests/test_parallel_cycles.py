"""Parallel cycles feature flag (COS-74)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def _cycle(
    client: AsyncClient, headers: dict, org_id: str, project_id: str, name: str
) -> dict:
    res = await client.post(
        f"{API}/orgs/{org_id}/projects/{project_id}/cycles",
        json={"name": name},
        headers=headers,
    )
    assert res.status_code in (200, 201), res.text
    return res.json()["data"]


async def test_single_active_by_default_and_parallel_flag(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    a = await _cycle(client, h, org["id"], project["id"], "Sprint A")
    b = await _cycle(client, h, org["id"], project["id"], "Sprint B")

    assert (await client.post(f"{pbase}/cycles/{a['id']}/start", headers=h)).status_code == 200
    blocked = await client.post(f"{pbase}/cycles/{b['id']}/start", headers=h)
    assert blocked.status_code == 400

    await client.patch(pbase, json={"features": {"parallel_cycles": True}}, headers=h)
    allowed = await client.post(f"{pbase}/cycles/{b['id']}/start", headers=h)
    assert allowed.status_code == 200, allowed.text
