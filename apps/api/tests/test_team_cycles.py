"""Teamspace cross-project cycles tracker (COS-95)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_team_cycles_aggregates_linked_projects(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    p1 = await create_project(client, h, org["id"], key="AAA", name="Alpha")
    p2 = await create_project(client, h, org["id"], key="BBB", name="Beta")

    team = (
        await client.post(f"{API}/orgs/{org['id']}/teams", json={"name": "Platform"}, headers=h)
    ).json()["data"]
    await client.put(
        f"{API}/orgs/{org['id']}/teams/{team['id']}/projects",
        json={"project_ids": [p1["id"], p2["id"]]},
        headers=h,
    )

    for project, name in ((p1, "P1 Sprint"), (p2, "P2 Sprint")):
        await client.post(
            f"{API}/orgs/{org['id']}/projects/{project['id']}/cycles",
            json={"name": name},
            headers=h,
        )

    res = await client.get(f"{API}/orgs/{org['id']}/teams/{team['id']}/cycles", headers=h)
    assert res.status_code == 200, res.text
    names = {c["name"] for c in res.json()["data"]}
    assert {"P1 Sprint", "P2 Sprint"} <= names
    assert all("project_key" in c for c in res.json()["data"])
