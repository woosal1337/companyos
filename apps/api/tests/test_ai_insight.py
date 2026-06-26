"""Heuristic project routing and context aggregation (TRI-04, MA-16)."""

from httpx import AsyncClient

from tests.helpers import (
    API,
    create_org,
    create_project,
    create_task,
    import_meeting,
    register_and_login,
)


async def test_route_suggests_the_keyword_matching_project(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    mobile = await create_project(client, auth["headers"], org["id"], key="MOB", name="Mobile App")
    billing = await create_project(
        client, auth["headers"], org["id"], key="BIL", name="Billing System"
    )
    task = await create_task(
        client,
        auth["headers"],
        org["id"],
        billing["id"],
        title="Fix the mobile app login screen",
    )
    response = await client.post(
        f"{API}/orgs/{org['id']}/ai/route",
        json={"kind": "task", "id": task["id"]},
        headers=auth["headers"],
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    assert data["project_id"] == mobile["id"]
    assert data["route"] == "Mobile App"
    assert data["confidence"] > 0


async def test_route_returns_null_when_nothing_matches(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    await create_project(client, auth["headers"], org["id"], key="MOB", name="Mobile App")
    project = await create_project(client, auth["headers"], org["id"], key="OPS", name="Operations")
    task = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Zzzqqq wibble frobnicate"
    )
    response = await client.post(
        f"{API}/orgs/{org['id']}/ai/route",
        json={"kind": "task", "id": task["id"]},
        headers=auth["headers"],
    )
    data = response.json()["data"]
    assert data["project_id"] is None
    assert data["route"] is None
    assert data["confidence"] == 0.0


async def test_context_surfaces_related_task_and_meeting(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="CTX")
    anchor = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Weekly sync planning agenda"
    )
    related = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Weekly sync follow up actions"
    )
    unrelated = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Quarterly budget spreadsheet"
    )
    meeting = await import_meeting(client, auth["headers"], org["id"])

    response = await client.get(
        f"{API}/orgs/{org['id']}/ai/context?kind=task&id={anchor['id']}",
        headers=auth["headers"],
    )
    assert response.status_code == 200, response.text
    data = response.json()["data"]
    found = {(signal["kind"], signal["id"]) for signal in data["signals"]}
    assert ("related_task", related["id"]) in found
    assert ("related_meeting", meeting["id"]) in found
    assert ("related_task", unrelated["id"]) not in found
    assert data["confidence"] > 0
    assert data["coverage"]["total"] >= 3
    assert data["coverage"]["consulted"] >= 2


async def test_context_is_empty_for_an_isolated_task(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"], key="ISO")
    anchor = await create_task(
        client, auth["headers"], org["id"], project["id"], title="Xylophone zucchini kumquat"
    )
    response = await client.get(
        f"{API}/orgs/{org['id']}/ai/context?kind=task&id={anchor['id']}",
        headers=auth["headers"],
    )
    data = response.json()["data"]
    assert data["signals"] == []
    assert data["confidence"] == 0.0
    assert data["coverage"]["consulted"] == 0
