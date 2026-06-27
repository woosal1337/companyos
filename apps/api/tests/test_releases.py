"""Release CRUD + task tagging tests (COS-70)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_release_crud_and_tagging(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="REL")
    base = f"{API}/orgs/{org['id']}/releases"

    created = await client.post(
        base,
        json={"name": "Summer launch", "version": "v1.2.0", "released_at": "2026-08-01"},
        headers=auth["headers"],
    )
    assert created.status_code == 201, created.text
    release = created.json()["data"]
    assert release["version"] == "v1.2.0"
    assert release["status"] == "planned"
    assert release["task_total"] == 0

    t1 = await create_task(client, auth["headers"], org["id"], project["id"], title="Ship A")
    t2 = await create_task(client, auth["headers"], org["id"], project["id"], title="Ship B")
    for task in (t1, t2):
        tagged = await client.post(
            f"{base}/{release['id']}/tasks/{task['id']}", headers=auth["headers"]
        )
        assert tagged.status_code == 201, tagged.text
    await client.post(
        f"{API}/orgs/{org['id']}/tasks/{t1['id']}/status",
        json={"status": "done"},
        headers=auth["headers"],
    )

    listing = await client.get(base, headers=auth["headers"])
    row = listing.json()["data"][0]
    assert row["task_total"] == 2
    assert row["task_done"] == 1

    scope = await client.get(f"{base}/{release['id']}/tasks", headers=auth["headers"])
    assert scope.status_code == 200, scope.text
    identifiers = {row["identifier"] for row in scope.json()["data"]}
    assert all(ident.startswith("REL-") for ident in identifiers)
    assert len(identifiers) == 2

    detail = await client.get(f"{base}/{release['id']}", headers=auth["headers"])
    assert detail.status_code == 200, detail.text
    assert detail.json()["data"]["task_total"] == 2
    with_log = await client.patch(
        f"{base}/{release['id']}",
        json={"changelog": "- Shipped A\n- Shipped B"},
        headers=auth["headers"],
    )
    assert with_log.json()["data"]["changelog"] == "- Shipped A\n- Shipped B"

    updated = await client.patch(
        f"{base}/{release['id']}", json={"status": "released"}, headers=auth["headers"]
    )
    assert updated.json()["data"]["status"] == "released"
    removed = await client.delete(
        f"{base}/{release['id']}/tasks/{t2['id']}", headers=auth["headers"]
    )
    assert removed.status_code == 200
    after = await client.get(base, headers=auth["headers"])
    assert after.json()["data"][0]["task_total"] == 1
