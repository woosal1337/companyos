"""RAID register / decision log / risk register (COS-261)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_register_crud_and_risk_score(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/register"

    risk = await client.post(
        base,
        json={"kind": "risk", "title": "Vendor SLA slip", "probability": 4, "impact": 5},
        headers=auth["headers"],
    )
    assert risk.status_code == 200, risk.text
    assert risk.json()["data"]["risk_score"] == 20

    decision = await client.post(
        base,
        json={"kind": "decision", "title": "Adopt Postgres", "description": "ADR-001"},
        headers=auth["headers"],
    )
    assert decision.status_code == 200
    assert decision.json()["data"]["risk_score"] is None

    await client.post(
        base, json={"kind": "dependency", "title": "Upstream API"}, headers=auth["headers"]
    )

    all_entries = await client.get(base, headers=auth["headers"])
    assert len(all_entries.json()["data"]) == 3
    risks = await client.get(f"{base}?kind=risk", headers=auth["headers"])
    assert [e["kind"] for e in risks.json()["data"]] == ["risk"]

    risk_id = risk.json()["data"]["id"]
    updated = await client.patch(
        f"{base}/{risk_id}",
        json={"status": "mitigated", "impact": 2},
        headers=auth["headers"],
    )
    assert updated.json()["data"]["status"] == "mitigated"
    assert updated.json()["data"]["risk_score"] == 8

    deleted = await client.delete(f"{base}/{risk_id}", headers=auth["headers"])
    assert deleted.status_code == 200
    assert len((await client.get(base, headers=auth["headers"])).json()["data"]) == 2


async def test_register_scoped_to_project(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    p1 = await create_project(client, auth["headers"], org["id"], key="PA")
    p2 = await create_project(client, auth["headers"], org["id"], key="PB")
    await client.post(
        f"{API}/orgs/{org['id']}/projects/{p1['id']}/register",
        json={"kind": "issue", "title": "Only in PA"},
        headers=auth["headers"],
    )
    other = await client.get(
        f"{API}/orgs/{org['id']}/projects/{p2['id']}/register", headers=auth["headers"]
    )
    assert other.json()["data"] == []
