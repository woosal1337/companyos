"""Config-as-code export + validate (COS-243)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_config_export_and_validate(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    await create_project(client, h, org["id"], key="CFG")
    await client.post(
        f"{API}/orgs/{org['id']}/labels", json={"name": "urgent", "color": "#ff0000"}, headers=h
    )

    export = await client.get(f"{API}/orgs/{org['id']}/config/export", headers=h)
    assert export.status_code == 200, export.text
    doc = export.json()["data"]
    assert doc["version"] == 1
    assert any(p["key"] == "CFG" for p in doc["projects"])
    assert any(label["name"] == "urgent" for label in doc["labels"])
    assert len(doc["workflow_statuses"]) > 0

    good = await client.post(f"{API}/orgs/{org['id']}/config/validate", json=doc, headers=h)
    assert good.json()["data"]["valid"] is True
    assert good.json()["data"]["errors"] == []

    bad = await client.post(
        f"{API}/orgs/{org['id']}/config/validate",
        json={"version": 1, "projects": [{"name": "no key"}]},
        headers=h,
    )
    assert bad.json()["data"]["valid"] is False
    assert len(bad.json()["data"]["errors"]) > 0
