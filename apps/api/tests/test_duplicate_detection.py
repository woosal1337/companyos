"""Duplicate detection + mark-not-duplicate (COS-242)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_duplicate_detection_and_suppression(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    pbase = f"{API}/orgs/{org['id']}/projects/{project['id']}"

    existing = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Fix login redirect loop"
    )
    await create_task(
        client, auth["headers"], org["id"], project["id"], title="Write release notes"
    )

    check = await client.get(
        f"{pbase}/tasks/duplicate-check",
        params={"title": "Fix the login redirect loop bug"},
        headers=auth["headers"],
    )
    assert check.status_code == 200, check.text
    candidates = check.json()["data"]
    assert existing["id"] in {c["task_id"] for c in candidates}
    assert all(c["shared_tokens"] >= 2 for c in candidates)

    dup = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Fix login redirect loop again"
    )
    marked = await client.post(
        f"{API}/orgs/{org['id']}/tasks/{dup['id']}/not-duplicate/{existing['id']}",
        headers=auth["headers"],
    )
    assert marked.status_code == 200, marked.text

    rechecked = await client.get(
        f"{pbase}/tasks/duplicate-check",
        params={"title": "Fix login redirect loop again", "exclude": dup["id"]},
        headers=auth["headers"],
    )
    assert existing["id"] not in {c["task_id"] for c in rechecked.json()["data"]}
