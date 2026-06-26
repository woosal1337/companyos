"""Workspace-level property templates + import into projects (COS-88)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_property_template_define_and_import(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    tbase = f"{API}/orgs/{org['id']}/property-templates"

    created = await client.post(
        tbase,
        json={"name": "Severity", "type": "select", "options": ["low", "high"]},
        headers=h,
    )
    assert created.status_code == 201, created.text
    template = created.json()["data"]

    listed = await client.get(tbase, headers=h)
    assert any(t["id"] == template["id"] for t in listed.json()["data"])

    imported = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/properties/import/{template['id']}",
        headers=h,
    )
    assert imported.status_code == 201, imported.text
    assert imported.json()["data"]["name"] == "Severity"
    assert imported.json()["data"]["options"] == ["low", "high"]

    again = await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/properties/import/{template['id']}",
        headers=h,
    )
    assert again.status_code == 400

    deleted = await client.delete(f"{tbase}/{template['id']}", headers=h)
    assert deleted.status_code == 200
