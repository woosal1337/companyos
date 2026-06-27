"""Task description edit history + restore (COS-148)."""

from httpx import AsyncClient

from tests.helpers import API, create_org, create_project, create_task, register_and_login


async def test_description_history_and_restore(client: AsyncClient) -> None:
    auth = await register_and_login(client)
    org = await create_org(client, auth["headers"])
    project = await create_project(client, auth["headers"], org["id"])
    task = await create_task(client, auth["headers"], org["id"], project["id"], title="Doc")
    base = f"{API}/orgs/{org['id']}/tasks/{task['id']}"

    assert (await client.get(f"{base}/description/versions", headers=auth["headers"])).json()[
        "data"
    ] == []

    await client.patch(base, json={"description": "v1"}, headers=auth["headers"])
    await client.patch(base, json={"description": "v2"}, headers=auth["headers"])
    await client.patch(base, json={"description": "v3"}, headers=auth["headers"])

    versions = (await client.get(f"{base}/description/versions", headers=auth["headers"])).json()[
        "data"
    ]
    assert [v["description"] for v in versions] == ["v2", "v1"]

    await client.patch(base, json={"description": "v3"}, headers=auth["headers"])
    assert (
        len(
            (await client.get(f"{base}/description/versions", headers=auth["headers"])).json()[
                "data"
            ]
        )
        == 2
    )

    v1_id = versions[1]["id"]
    restored = await client.post(
        f"{base}/description/versions/{v1_id}/restore", headers=auth["headers"]
    )
    assert restored.status_code == 200, restored.text
    assert restored.json()["data"]["description"] == "v1"
    after = (await client.get(f"{base}/description/versions", headers=auth["headers"])).json()[
        "data"
    ]
    assert after[0]["description"] == "v3"
    assert len(after) == 3
