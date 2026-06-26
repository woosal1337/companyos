"""Team-scoped pages / team knowledge hub (COS-84)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_team_scoped_pages(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    team = (
        await client.post(
            f"{API}/orgs/{org['id']}/teams", json={"name": "Platform"}, headers=auth["headers"]
        )
    ).json()["data"]

    notes_url = f"{API}/orgs/{org['id']}/notes"
    team_page = await client.post(
        notes_url,
        json={"title": "Runbook", "content": "## Steps", "team_id": team["id"]},
        headers=auth["headers"],
    )
    assert team_page.status_code == 201, team_page.text
    assert team_page.json()["data"]["team_id"] == team["id"]

    await client.post(notes_url, json={"title": "Loose note"}, headers=auth["headers"])

    scoped = await client.get(f"{notes_url}?team_id={team['id']}", headers=auth["headers"])
    items = scoped.json()["data"]["items"]
    assert [n["title"] for n in items] == ["Runbook"]

    everything = await client.get(notes_url, headers=auth["headers"])
    assert {n["title"] for n in everything.json()["data"]["items"]} >= {"Runbook", "Loose note"}
