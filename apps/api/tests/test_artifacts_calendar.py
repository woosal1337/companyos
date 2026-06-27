"""Project artifacts (MA-17) and event linked-notes counts (CAL-02-BE)."""

from datetime import UTC, datetime, timedelta

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_project_artifact_crud(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="ART")
    base = f"{API}/orgs/{org['id']}/projects/{project['id']}/artifacts"

    added = await client.post(
        base, json={"label": "Figma", "url": "https://figma.com/x"}, headers=auth["headers"]
    )
    assert added.status_code == 201, added.text
    artifact_id = added.json()["data"]["id"]

    listing = await client.get(base, headers=auth["headers"])
    assert [a["label"] for a in listing.json()["data"]] == ["Figma"]

    deleted = await client.delete(f"{base}/{artifact_id}", headers=auth["headers"])
    assert deleted.status_code == 200, deleted.text
    assert (await client.get(base, headers=auth["headers"])).json()["data"] == []


async def test_event_exposes_linked_meeting_and_notes_count(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CAL")
    await client.post(
        f"{API}/orgs/{org['id']}/notes",
        json={"title": "Spec", "content": "details", "project_id": project["id"]},
        headers=auth["headers"],
    )
    meeting = await client.post(
        f"{API}/orgs/{org['id']}/meetings",
        json={
            "title": "Sync",
            "started_at": datetime.now(UTC).isoformat(),
            "project_id": project["id"],
        },
        headers=auth["headers"],
    )
    meeting_id = meeting.json()["data"]["id"]
    start = datetime.now(UTC) + timedelta(days=1)
    event = await client.post(
        f"{API}/orgs/{org['id']}/events",
        json={
            "title": "Planning",
            "starts_at": start.isoformat(),
            "ends_at": (start + timedelta(hours=1)).isoformat(),
            "visibility": "team",
            "meeting_id": meeting_id,
        },
        headers=auth["headers"],
    )
    event_id = event.json()["data"]["id"]

    got = await client.get(f"{API}/orgs/{org['id']}/events/{event_id}", headers=auth["headers"])
    data = got.json()["data"]
    assert data["linked_meeting_id"] == meeting_id
    assert data["linked_notes_count"] == 1
