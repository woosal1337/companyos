"""Email-to-task intake (COS-62)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_email_intake_to_triage_task(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], key="MAIL")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/email-intake"

    created = await client.post(base, headers=h)
    assert created.status_code == 201, created.text
    token = created.json()["data"]["token"]
    assert created.json()["data"]["enabled"] is True

    ingest = await client.post(
        f"{API}/integrations/email/{token}",
        json={"subject": "Bug: login fails", "from": "user@acme.com", "text": "Steps to repro..."},
    )
    assert ingest.status_code == 201, ingest.text
    ref = ingest.json()["data"]["reference"]
    assert ref.startswith("MAIL-")

    triage = await client.get(f"{API}/orgs/{org['id']}/triage", headers=h)
    items = (
        triage.json()["data"]["items"]
        if isinstance(triage.json()["data"], dict)
        else triage.json()["data"]
    )
    match = next((t for t in items if t["title"] == "Bug: login fails"), None)
    assert match is not None
    assert match["intake_channel"] == "email"
    assert match["is_triage"] is True

    assert len((await client.get(base, headers=h)).json()["data"]) == 1
    iid = created.json()["data"]["id"]
    assert (await client.delete(f"{base}/{iid}", headers=h)).status_code == 200
    assert (
        await client.post(f"{API}/integrations/email/{token}", json={"subject": "x"})
    ).status_code == 404
