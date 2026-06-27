"""Release changelog entries (COS-269)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_changelog_crud_and_categories(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    rbase = f"{API}/orgs/{org['id']}/releases"

    release = (
        await client.post(rbase, json={"name": "v1.0", "version": "1.0.0"}, headers=h)
    ).json()["data"]

    added = await client.post(
        f"{rbase}/{release['id']}/changelog",
        json={"category": "added", "title": "Dark mode", "pr_url": "https://example.com/pr/1"},
        headers=h,
    )
    assert added.status_code == 201, added.text
    entry = added.json()["data"]
    assert entry["category"] == "added"

    await client.post(
        f"{rbase}/{release['id']}/changelog",
        json={"category": "security", "title": "Patched XSS"},
        headers=h,
    )

    listed = await client.get(f"{rbase}/{release['id']}/changelog", headers=h)
    cats = {e["category"] for e in listed.json()["data"]}
    assert {"added", "security"} <= cats

    updated = await client.patch(
        f"{rbase}/changelog/{entry['id']}", json={"category": "changed"}, headers=h
    )
    assert updated.json()["data"]["category"] == "changed"

    deleted = await client.delete(f"{rbase}/changelog/{entry['id']}", headers=h)
    assert deleted.status_code == 200
