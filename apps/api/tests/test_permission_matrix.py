"""Per-resource permission matrix + enforcement (COS-182)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    create_task,
    register_and_login,
)


async def test_matrix_denies_comment_delete(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    oh = owner["headers"]
    org = await create_org(client, oh)
    member = await register_and_login(client)
    await add_org_member(client, oh, org["id"], member)
    mh = member["headers"]
    member_me = (await client.get(f"{API}/users/me", headers=mh)).json()["data"]

    perms = await client.get(f"{API}/orgs/{org['id']}/roles/permissions", headers=oh)
    assert perms.status_code == 200, perms.text
    assert any(r["resource"] == "comments" for r in perms.json()["data"]["matrix_schema"])
    assert "own" in perms.json()["data"]["matrix_cells"]

    role = await client.post(
        f"{API}/orgs/{org['id']}/roles",
        json={
            "name": "Restricted",
            "permissions": ["tasks.create"],
            "matrix": {"comments": {"delete": "none"}, "bogus": {"x": "y"}},
        },
        headers=oh,
    )
    assert role.status_code == 201, role.text
    assert role.json()["data"]["matrix"] == {"comments": {"delete": "none"}}
    await client.post(
        f"{API}/orgs/{org['id']}/roles/assign",
        json={"user_id": member_me["id"], "custom_role_id": role.json()["data"]["id"]},
        headers=oh,
    )

    project = await create_project(client, oh, org["id"], key="MAT")
    await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members",
        json={"user_id": member_me["id"], "role": "member"},
        headers=oh,
    )
    task = await create_task(client, mh, org["id"], project["id"], title="t")
    comment = await client.post(
        f"{API}/orgs/{org['id']}/comments",
        json={"entity_type": "task", "entity_id": task["id"], "content": "hi"},
        headers=mh,
    )
    cid = comment.json()["data"]["id"]

    denied = await client.delete(f"{API}/orgs/{org['id']}/comments/{cid}", headers=mh)
    assert denied.status_code == 403, denied.text

    allowed = await client.delete(f"{API}/orgs/{org['id']}/comments/{cid}", headers=oh)
    assert allowed.status_code == 200, allowed.text
