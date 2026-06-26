"""Milestone grouping cycles/modules under one deadline (COS-128)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_milestone_aggregates_cycle_and_module(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    milestone = (
        await client.post(f"{pbase}/milestones", json={"name": "Launch"}, headers=h)
    ).json()["data"]
    cycle = (await client.post(f"{pbase}/cycles", json={"name": "Sprint"}, headers=h)).json()[
        "data"
    ]
    module = (await client.post(f"{pbase}/modules", json={"name": "Billing"}, headers=h)).json()[
        "data"
    ]

    await client.patch(
        f"{pbase}/cycles/{cycle['id']}", json={"milestone_id": milestone["id"]}, headers=h
    )
    await client.patch(
        f"{pbase}/modules/{module['id']}", json={"milestone_id": milestone["id"]}, headers=h
    )

    t1 = await create_task(client, h, org["id"], project["id"])
    t2 = await create_task(client, h, org["id"], project["id"])
    await client.post(f"{pbase}/cycles/{cycle['id']}/tasks/{t1['id']}", headers=h)
    await client.post(f"{pbase}/modules/{module['id']}/tasks/{t2['id']}", headers=h)

    listed = await client.get(f"{pbase}/milestones", headers=h)
    target = next(m for m in listed.json()["data"] if m["id"] == milestone["id"])
    assert target["task_total"] >= 2
