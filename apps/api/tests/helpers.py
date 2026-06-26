"""Shared async helpers for API-driven test setup."""

import uuid
from datetime import UTC, datetime
from typing import Any

from httpx import AsyncClient

API = "/api/v1"


async def register_and_login(
    client: AsyncClient, email: str | None = None, password: str = "password123"
) -> dict[str, Any]:
    """Register a fresh user, log in, and return headers plus identity."""
    email = email or f"user-{uuid.uuid4().hex[:10]}@test.dev"
    register = await client.post(
        f"{API}/auth/register",
        json={"email": email, "password": password, "full_name": "Test User"},
    )
    assert register.status_code == 201, register.text
    login = await client.post(f"{API}/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200, login.text
    data = login.json()["data"]
    token = data["tokens"]["access_token"]
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "user_id": data["user"]["id"],
        "email": email,
        "tokens": data["tokens"],
    }


async def create_org(
    client: AsyncClient, headers: dict[str, str], name: str = "Acme"
) -> dict[str, Any]:
    """Create an organization and return its payload."""
    response = await client.post(f"{API}/orgs", json={"name": name}, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()["data"]


async def create_project(
    client: AsyncClient,
    headers: dict[str, str],
    org_id: str,
    key: str = "DEMO",
    name: str = "Demo Project",
) -> dict[str, Any]:
    """Create a project and return its payload."""
    response = await client.post(
        f"{API}/orgs/{org_id}/projects", json={"name": name, "key": key}, headers=headers
    )
    assert response.status_code == 201, response.text
    return response.json()["data"]


async def create_task(
    client: AsyncClient,
    headers: dict[str, str],
    org_id: str,
    project_id: str,
    title: str = "A task",
    **extra: Any,
) -> dict[str, Any]:
    """Create a task and return its payload."""
    response = await client.post(
        f"{API}/orgs/{org_id}/projects/{project_id}/tasks",
        json={"title": title, **extra},
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return response.json()["data"]


def folio_payload(segment_count: int = 4) -> dict[str, Any]:
    """Build a Folio import payload with the given number of segments."""
    return {
        "title": "Weekly sync",
        "started_at": datetime.now(UTC).isoformat(),
        "duration_seconds": 1800,
        "attendees": ["External Guest"],
        "markdown": "# Weekly sync",
        "segments": [
            {
                "speaker": f"Speaker {index % 2 + 1}",
                "start_seconds": index * 10.0,
                "end_seconds": index * 10.0 + 9.5,
                "text": f"Segment text number {index}",
            }
            for index in range(segment_count)
        ],
    }


async def import_meeting(
    client: AsyncClient, headers: dict[str, str], org_id: str, segment_count: int = 4
) -> dict[str, Any]:
    """Import a Folio meeting and return its payload."""
    response = await client.post(
        f"{API}/orgs/{org_id}/meetings/import",
        json=folio_payload(segment_count),
        headers=headers,
    )
    assert response.status_code == 201, response.text
    return response.json()["data"]


async def add_org_member(
    client: AsyncClient,
    owner_headers: dict[str, str],
    org_id: str,
    member_client_auth: dict[str, Any],
    role: str = "member",
) -> None:
    """Invite and accept a second user into an org."""
    invite = await client.post(
        f"{API}/orgs/{org_id}/invites",
        json={"email": member_client_auth["email"], "role": role},
        headers=owner_headers,
    )
    assert invite.status_code == 201, invite.text
    token = invite.json()["data"]["token"]
    accept = await client.post(
        f"{API}/invites/accept", json={"token": token}, headers=member_client_auth["headers"]
    )
    assert accept.status_code == 200, accept.text
