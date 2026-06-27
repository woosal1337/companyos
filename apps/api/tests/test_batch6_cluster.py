"""Project metadata (MA-17), note activity excerpts (ACT-04), vocab activity (VOCA-BE-01)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_project_exposes_lead_and_target_date(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    created = await client.post(
        f"{API}/orgs/{org['id']}/projects",
        json={
            "name": "Apollo",
            "key": "APO",
            "lead_id": auth["user_id"],
            "target_date": "2026-12-31",
        },
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    data = created.json()["data"]
    assert data["lead_id"] == auth["user_id"]
    assert data["target_date"] == "2026-12-31"

    updated = await client.patch(
        f"{API}/orgs/{org['id']}/projects/{data['id']}",
        json={"target_date": "2027-01-15"},
        headers=auth["headers"],
    )
    assert updated.json()["data"]["target_date"] == "2027-01-15"


async def test_note_activity_carries_excerpt(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    note = await client.post(
        f"{API}/orgs/{org['id']}/notes",
        json={"title": "Roadmap", "content": "# Heading\nWe will ship the redesign in Q3."},
        headers=auth["headers"],
    )
    note_id = note.json()["data"]["id"]
    feed = await client.get(
        f"{API}/orgs/{org['id']}/activity/note/{note_id}", headers=auth["headers"]
    )
    created_event = next(e for e in feed.json()["data"]["items"] if e["event_type"] == "created")
    assert created_event["payload"]["excerpt"] == "Heading"


async def test_vocabulary_mutation_records_activity(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    term = await client.post(
        f"{API}/orgs/{org['id']}/vocabulary",
        json={"term": "ARR", "definition": "Annual recurring revenue"},
        headers=auth["headers"],
    )
    assert term.status_code == 201, term.text
    term_id = term.json()["data"]["id"]
    feed = await client.get(
        f"{API}/orgs/{org['id']}/activity/vocabulary/{term_id}", headers=auth["headers"]
    )
    event_types = [e["event_type"] for e in feed.json()["data"]["items"]]
    assert "created" in event_types
