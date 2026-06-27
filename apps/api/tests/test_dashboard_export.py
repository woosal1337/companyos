"""Dashboard printable HTML export for PDF (COS-139)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_dashboard_export_html(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"])
    await create_task(client, h, org["id"], project["id"], title="X")
    base = f"{API}/orgs/{org['id']}/dashboards"
    did = (await client.post(base, json={"name": "Quarterly"}, headers=h)).json()["data"]["id"]
    await client.post(
        f"{base}/{did}/widgets",
        json={
            "title": "Status mix",
            "config": {"chart_type": "bar", "metric": "count", "dimension": "status"},
        },
        headers=h,
    )

    res = await client.get(f"{base}/{did}/export.html", headers=h)
    assert res.status_code == 200, res.text
    assert "text/html" in res.headers["content-type"]
    body = res.text
    assert "Quarterly" in body
    assert "Status mix" in body
    assert "window.print()" in body
