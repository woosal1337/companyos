"""Custom directional relation types (COS-53)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_custom_relation_type_directional_labels(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    base = f"{API}/orgs/{org['id']}"

    defined = await client.post(
        f"{base}/relation-types",
        json={
            "name": "implements",
            "outward_label": "implements",
            "inward_label": "implemented by",
        },
        headers=auth["headers"],
    )
    assert defined.status_code == 201, defined.text
    type_id = defined.json()["data"]["id"]
    assert defined.json()["data"]["inward_label"] == "implemented by"

    a = await create_task(client, auth["headers"], org["id"], project["id"], title="A")
    b = await create_task(client, auth["headers"], org["id"], project["id"], title="B")

    rel = await client.post(
        f"{base}/tasks/{a['id']}/relations",
        json={"target_task_id": b["id"], "custom_type_id": type_id},
        headers=auth["headers"],
    )
    assert rel.status_code == 201, rel.text

    a_rels = await client.get(f"{base}/tasks/{a['id']}/relations", headers=auth["headers"])
    assert [r["type"] for r in a_rels.json()["data"]] == ["implements"]

    b_rels = await client.get(f"{base}/tasks/{b['id']}/relations", headers=auth["headers"])
    assert [r["type"] for r in b_rels.json()["data"]] == ["implemented by"]

    dupe = await client.post(
        f"{base}/tasks/{a['id']}/relations",
        json={"target_task_id": b["id"], "custom_type_id": type_id},
        headers=auth["headers"],
    )
    assert dupe.status_code == 409

    listed = await client.get(f"{base}/relation-types", headers=auth["headers"])
    assert type_id in {t["id"] for t in listed.json()["data"]}
    deleted = await client.delete(f"{base}/relation-types/{type_id}", headers=auth["headers"])
    assert deleted.status_code == 200
