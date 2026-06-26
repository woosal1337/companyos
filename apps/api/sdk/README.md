# CompanyOS SDKs (COS-219)

Typed clients for the [CompanyOS public REST API](../) (`/api/v1`, OpenAPI at
`/api/v1/docs`). Both authenticate with a **personal access token** sent as the
`x-api-key` header, or a **client-credentials bot token** from a confidential
OAuth app.

## Python (`sdk/python/companyos.py`)

```python
from companyos_sdk import CompanyOSClient

with CompanyOSClient("https://api.companyos.dev", token="cos_pat_...") as cos:
    me = cos.me()
    for project in cos.projects(org_id):
        print(project["name"])
    cos.create_task(org_id, project_id, "Investigate latency", priority="high")
```

Bot token (OAuth client_credentials):

```python
token = CompanyOSClient.bot_token(base_url, client_id="app-...", client_secret="cos_secret_...")
cos = CompanyOSClient(base_url, token=token)
```

Requires `httpx`.

## Node / TypeScript (`sdk/node/companyos.ts`)

```ts
import { CompanyOSClient } from "./companyos";

const cos = new CompanyOSClient("https://api.companyos.dev", "cos_pat_...");
const me = await cos.me();
const projects = await cos.projects(orgId);
await cos.createTask(orgId, projectId, "Investigate latency", { priority: "high" });
```

Uses the global `fetch` (Node 18+ / browsers). No runtime dependencies.

## Coverage

Both SDKs cover: `me`, `orgs`, `projects`/`createProject`, `tasks`/`createTask`,
`search`, `pql`, plus the `botToken` OAuth helper. They are thin, hand-written
clients over the stable REST surface; extend by adding methods that mirror the
documented endpoints.
