"""Liveness / readiness probes (COS-259)."""

from httpx import AsyncClient

from tests.helpers import API


async def test_livez_readyz(client: AsyncClient) -> None:
    live = await client.get(f"{API}/livez")
    assert live.status_code == 200, live.text
    assert live.json()["data"]["status"] == "alive"

    ready = await client.get(f"{API}/readyz")
    assert ready.status_code == 200, ready.text
    assert ready.json()["data"]["status"] == "ready"
    assert ready.json()["data"]["database"] is True
