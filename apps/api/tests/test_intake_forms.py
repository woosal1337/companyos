"""Custom intake forms (COS-51)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_intake_form_build_and_public_submit(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/intake-forms"

    created = await client.post(
        base,
        json={
            "name": "Bug report",
            "fields": [
                {"label": "Steps to reproduce", "type": "textarea", "required": True},
                {"label": "Severity", "type": "select", "options": ["low", "high"]},
            ],
        },
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    form = created.json()["data"]
    token = form["token"]
    assert form["fields"][0]["key"] == "steps_to_reproduce"

    public = await client.get(f"{API}/intake-forms/{token}")
    assert public.status_code == 200, public.text
    assert "token" not in public.json()["data"]

    bad = await client.post(
        f"{API}/intake-forms/{token}",
        json={"title": "It broke", "answers": {"severity": "high"}},
    )
    assert bad.status_code == 400

    ok_submit = await client.post(
        f"{API}/intake-forms/{token}",
        json={"title": "Login broke", "answers": {"steps_to_reproduce": "click login"}},
    )
    assert ok_submit.status_code == 201, ok_submit.text
    assert ok_submit.json()["data"]["reference"].startswith(project["key"])

    triage = await client.get(f"{API}/orgs/{org['id']}/triage", headers=auth["headers"])
    assert any(t["title"] == "Login broke" for t in triage.json()["data"])

    await client.patch(f"{base}/{form['id']}", json={"enabled": False}, headers=auth["headers"])
    assert (await client.get(f"{API}/intake-forms/{token}")).status_code == 404
