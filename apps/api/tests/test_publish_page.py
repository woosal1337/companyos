"""Publish a page to a public web link with anonymous comments (COS-124)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_publish_page_with_anonymous_comments(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    note = await client.post(
        f"{API}/orgs/{org['id']}/notes",
        json={"title": "Public RFC", "content": "# Heading\n\nSome **bold** text."},
        headers=h,
    )
    assert note.status_code in (200, 201), note.text
    note_id = note.json()["data"]["id"]

    published = await client.post(f"{API}/orgs/{org['id']}/notes/{note_id}/publish", headers=h)
    assert published.status_code == 200, published.text
    token = published.json()["data"]["public_token"]
    assert token

    page = await client.get(f"{API}/public/pages/{token}")
    assert page.status_code == 200, page.text
    body = page.json()["data"]
    assert body["title"] == "Public RFC"
    assert "<strong>bold</strong>" in body["content_html"]
    assert body["comments"] == []

    comment = await client.post(
        f"{API}/public/pages/{token}/comments",
        json={"author_name": "Guest", "body": "Nice page"},
    )
    assert comment.status_code == 201, comment.text
    comment_id = comment.json()["data"]["id"]
    after = await client.get(f"{API}/public/pages/{token}")
    assert len(after.json()["data"]["comments"]) == 1

    await client.post(f"{API}/public/pages/{token}/comments/{comment_id}/report")
    hidden = await client.get(f"{API}/public/pages/{token}")
    assert hidden.json()["data"]["comments"] == []

    await client.delete(f"{API}/orgs/{org['id']}/notes/{note_id}/publish", headers=h)
    assert (await client.get(f"{API}/public/pages/{token}")).status_code == 404
