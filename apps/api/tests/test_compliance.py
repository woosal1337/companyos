"""Compliance posture + GDPR export + erasure request (COS-233)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_compliance_posture_export_erasure(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    me = (await client.get(f"{API}/users/me", headers=h)).json()["data"]

    upd = await client.patch(
        f"{API}/orgs/{org['id']}",
        json={
            "residency_region": "eu",
            "compliance_frameworks": ["gdpr", "soc2"],
            "dpo_contact": "dpo@acme.com",
        },
        headers=h,
    )
    assert upd.status_code == 200, upd.text
    assert upd.json()["data"]["residency_region"] == "eu"
    assert set(upd.json()["data"]["compliance_frameworks"]) == {"gdpr", "soc2"}

    posture = await client.get(f"{API}/orgs/{org['id']}/compliance", headers=h)
    assert posture.json()["data"]["dpo_contact"] == "dpo@acme.com"

    export = await client.get(
        f"{API}/orgs/{org['id']}/compliance/data-subjects/{me['id']}/export", headers=h
    )
    assert export.status_code == 200, export.text
    assert export.json()["data"]["subject"]["email"] == me["email"]
    assert "authored_tasks" in export.json()["data"]["content"]

    erase = await client.post(
        f"{API}/orgs/{org['id']}/compliance/erasure-requests",
        json={"user_id": me["id"], "reason": "test"},
        headers=h,
    )
    assert erase.status_code == 200, erase.text
    assert erase.json()["data"]["status"] == "pending_review"
