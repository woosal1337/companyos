"""Page (note) templates (COS-245)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def _create_note(client: AsyncClient, headers: dict[str, str], org_id: str, **body: object):
    payload = {"title": "Doc", "content": "# Heading\n\nBody", **body}
    return await client.post(f"{API}/orgs/{org_id}/notes", json=payload, headers=headers)


async def test_note_templates_crud_and_save_from_note(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    base = f"{API}/orgs/{org['id']}/note-templates"

    created = await client.post(
        base,
        json={"name": "Meeting notes", "title": "Meeting — ", "content": "## Agenda\n## Actions"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    assert created.json()["data"]["content"] == "## Agenda\n## Actions"

    dupe = await client.post(
        base, json={"name": "Meeting notes", "title": "x"}, headers=auth["headers"]
    )
    assert dupe.status_code == 409

    note = await _create_note(client, auth["headers"], org["id"], project_id=project["id"])
    assert note.status_code == 201, note.text
    saved = await client.post(
        f"{base}/from-note/{note.json()['data']['id']}",
        json={"name": "From doc"},
        headers=auth["headers"],
    )
    assert saved.status_code == 201, saved.text
    assert saved.json()["data"]["project_id"] == project["id"]
    assert saved.json()["data"]["content"] == "# Heading\n\nBody"

    scoped = await client.get(f"{base}?project_id={project['id']}", headers=auth["headers"])
    names = {t["name"] for t in scoped.json()["data"]}
    assert names == {"Meeting notes", "From doc"}

    org_only = await client.get(base, headers=auth["headers"])
    assert {t["name"] for t in org_only.json()["data"]} == {"Meeting notes"}

    deleted = await client.delete(f"{base}/{created.json()['data']['id']}", headers=auth["headers"])
    assert deleted.status_code == 200
