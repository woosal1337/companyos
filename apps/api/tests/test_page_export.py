"""Page export to Markdown/HTML (COS-130)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, register_and_login


async def test_page_export_markdown_and_html(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    note = (
        await client.post(
            f"{API}/orgs/{org['id']}/notes",
            json={"title": "My Page", "content": "## Heading\n\n**bold** text\n- one\n- two"},
            headers=h,
        )
    ).json()["data"]

    md = await client.get(f"{API}/orgs/{org['id']}/notes/{note['id']}/export.md", headers=h)
    assert md.status_code == 200, md.text
    assert md.headers["content-type"].startswith("text/markdown")
    assert "# My Page" in md.text
    assert "**bold**" in md.text
    assert "My Page.md" in md.headers["content-disposition"]

    html_res = await client.get(f"{API}/orgs/{org['id']}/notes/{note['id']}/export.html", headers=h)
    assert html_res.status_code == 200, html_res.text
    assert html_res.headers["content-type"].startswith("text/html")
    assert "<h2>Heading</h2>" in html_res.text
    assert "<strong>bold</strong>" in html_res.text
    assert "<li>one</li>" in html_res.text
