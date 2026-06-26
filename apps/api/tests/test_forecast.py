"""Throughput forecast analytics (COS-194)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, register_and_login


async def test_throughput_forecast_shape(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])

    forecast = await client.get(
        f"{API}/orgs/{org['id']}/analytics/forecast",
        params={"weeks": 6, "project_id": project["id"]},
        headers=auth["headers"],
    )
    assert forecast.status_code == 200, forecast.text
    data = forecast.json()["data"]
    assert len(data["weekly"]) == 6
    assert all("week_start" in week and "completed" in week for week in data["weekly"])
    assert data["avg_per_week"] >= 0
    assert data["projected_next_week"] >= 0
