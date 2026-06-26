"""Unified multi-entity search (COS-253)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_search_across_entities(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    h = auth["headers"]
    org = await create_org(client, h)
    project = await create_project(client, h, org["id"], name="Payments Platform", key="PAY")
    await create_task(client, h, org["id"], project["id"], title="Fix payment webhook retry")
    await create_task(client, h, org["id"], project["id"], title="Unrelated chore")

    res = await client.get(f"{API}/orgs/{org['id']}/search", params={"q": "payment"}, headers=h)
    assert res.status_code == 200, res.text
    data = res.json()["data"]
    assert data["query"] == "payment"
    titles = [r["title"] for r in data["results"]]
    assert "Payments Platform" in titles
    assert "Fix payment webhook retry" in titles
    assert "Unrelated chore" not in titles
    scores = [r["score"] for r in data["results"]]
    assert scores == sorted(scores, reverse=True)
    task_hit = next(r for r in data["results"] if r["type"] == "task")
    assert task_hit["identifier"].startswith("PAY-")

    only_tasks = await client.get(
        f"{API}/orgs/{org['id']}/search", params={"q": "payment", "types": "task"}, headers=h
    )
    assert {r["type"] for r in only_tasks.json()["data"]["results"]} == {"task"}
