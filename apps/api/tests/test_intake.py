"""Public intake form tests (COS-32)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_multi_channel_intake(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="MCI")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/intake"

    blocked = await client.post(
        f"{base}/submit", json={"title": "Need help"}, headers=auth["headers"]
    )
    assert blocked.status_code == 404, blocked.text

    enabled = await client.post(f"{base}/inapp/enable", headers=auth["headers"])
    assert enabled.status_code == 200, enabled.text
    assert enabled.json()["data"]["intake_inapp_enabled"] is True

    submitted = await client.post(
        f"{base}/submit", json={"title": "Need help"}, headers=auth["headers"]
    )
    assert submitted.status_code == 200, submitted.text
    task = submitted.json()["data"]
    assert task["is_triage"] is True
    assert task["intake_channel"] == "in_app"

    triage = await client.get(f"{API}/orgs/{org['id']}/triage", headers=auth["headers"])
    item = next(t for t in triage.json()["data"] if t["id"] == task["id"])
    assert item["intake_channel"] == "in_app"

    token = (await client.post(f"{base}/enable", headers=auth["headers"])).json()["data"][
        "intake_token"
    ]
    await client.post(f"{API}/intake/{token}", json={"title": "From the web"})
    triage2 = await client.get(f"{API}/orgs/{org['id']}/triage", headers=auth["headers"])
    channels = {t["title"]: t["intake_channel"] for t in triage2.json()["data"]}
    assert channels["From the web"] == "form"


async def test_public_intake_submission(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="INT")
    admin_base = f"{API}/orgs/{org['id']}/projects/{project['id']}/intake"

    enabled = await client.post(f"{admin_base}/enable", headers=auth["headers"])
    assert enabled.status_code == 200, enabled.text
    token = enabled.json()["data"]["intake_token"]
    assert token

    form = await client.get(f"{API}/intake/{token}")
    assert form.status_code == 200, form.text
    assert form.json()["data"]["project_name"] == "Demo Project"

    submit = await client.post(
        f"{API}/intake/{token}",
        json={"title": "Bug from a customer", "submitter_email": "user@example.com"},
    )
    assert submit.status_code == 200, submit.text
    reference = submit.json()["data"]["reference"]
    assert reference.startswith("INT-")

    triage = await client.get(f"{API}/orgs/{org['id']}/triage", headers=auth["headers"])
    titles = {item["title"] for item in triage.json()["data"]}
    assert "Bug from a customer" in titles

    await client.post(f"{admin_base}/disable", headers=auth["headers"])
    assert (await client.get(f"{API}/intake/{token}")).status_code == 404
    assert (
        await client.post(f"{API}/intake/{token}", json={"title": "Too late"})
    ).status_code == 404


async def test_intake_unknown_token_is_404(client: AsyncClient) -> None:
    assert (await client.get(f"{API}/intake/nope-not-a-token")).status_code == 404
