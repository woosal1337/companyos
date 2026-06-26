"""RBAC audit trail (COS-189)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    add_org_member,
    create_org,
    create_project,
    register_and_login,
)


async def _audit(client: AsyncClient, org_id: str, headers: dict, **params: str) -> list[dict]:
    resp = await client.get(f"{API}/orgs/{org_id}/rbac-audit", params=params, headers=headers)
    assert resp.status_code == 200, resp.text
    return resp.json()["data"]["items"]


async def test_org_role_change_audited_with_before_after(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    member_id = (await client.get(f"{API}/users/me", headers=member["headers"])).json()["data"][
        "id"
    ]

    await client.patch(
        f"{API}/orgs/{org['id']}/members/{member_id}",
        json={"role": "admin"},
        headers=owner["headers"],
    )
    items = await _audit(client, org["id"], owner["headers"], action="org_role_changed")
    assert len(items) == 1
    row = items[0]
    assert row["role_before"] == "member"
    assert row["role_after"] == "admin"
    assert row["subject_user_id"] == member_id
    assert row["actor_id"] == owner["user_id"]
    assert row["resource_scope"] == "org"
    assert row["actor_type"] == "user"


async def test_project_role_change_audited(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    project = await create_project(client, owner["headers"], org["id"], key="AUD")
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")
    member_id = (await client.get(f"{API}/users/me", headers=member["headers"])).json()["data"][
        "id"
    ]
    await client.post(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members",
        json={"user_id": member_id, "role": "member"},
        headers=owner["headers"],
    )
    await client.patch(
        f"{API}/orgs/{org['id']}/projects/{project['id']}/members/{member_id}",
        json={"role": "admin"},
        headers=owner["headers"],
    )
    items = await _audit(client, org["id"], owner["headers"], action="project_role_changed")
    assert len(items) == 1
    assert items[0]["role_before"] == "member"
    assert items[0]["role_after"] == "admin"
    assert items[0]["project_id"] == project["id"]

    added = await _audit(
        client, org["id"], owner["headers"], action="member_added", resource_scope="project"
    )
    assert any(r["subject_user_id"] == member_id for r in added)


async def test_rbac_audit_admin_only_and_filterable(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")

    denied = await client.get(f"{API}/orgs/{org['id']}/rbac-audit", headers=member["headers"])
    assert denied.status_code == 403, denied.text

    member_id = (await client.get(f"{API}/users/me", headers=member["headers"])).json()["data"][
        "id"
    ]
    invited = await _audit(client, org["id"], owner["headers"], action="member_invited")
    assert len(invited) == 1
    assert invited[0]["subject_user_id"] is None
    assert invited[0]["role_after"] == "member"
    assert invited[0]["detail"]["email"] == member["email"]
    added = await _audit(
        client, org["id"], owner["headers"], subject_user_id=member_id, action="member_added"
    )
    assert len(added) == 1
    assert added[0]["subject_user_id"] == member_id


async def test_rbac_audit_csv_export(client: AsyncClient) -> None:
    owner = await register_and_login(client)
    org = await create_org(client, owner["headers"])
    member = await register_and_login(client)
    await add_org_member(client, owner["headers"], org["id"], member, role="member")

    export = await client.get(
        f"{API}/orgs/{org['id']}/rbac-audit/export.csv", headers=owner["headers"]
    )
    assert export.status_code == 200, export.text
    assert export.headers["content-type"].startswith("text/csv")
    body = export.text
    assert "timestamp,actor,actor_type,subject,scope,resource_id,action" in body
    assert "member_invited" in body
