# Contributing to CompanyOS

Thanks for your interest in CompanyOS. This guide covers how to get the project
running and what we expect in a pull request.

## Repository layout

CompanyOS is a monorepo with two deployable apps:

- `apps/api` — Python / FastAPI backend (uv, Ruff, mypy, pytest, Alembic).
- `apps/web` — Next.js web app in a Bun + Turborepo workspace.

## Run it locally

The fastest path is the full stack with Docker:

```bash
cp .env.example .env
docker compose up --build
```

The web app is on http://localhost:3000 and the API on http://localhost:8000.

To work on an app directly:

- **Backend:** `cd apps/api && uv sync && uv run uvicorn companyos.main:app --reload`
- **Web:** `cd apps/web && bun install && bun run dev`

## Checks must pass

Before opening a pull request, run the same checks CI runs.

**Backend** (`apps/api`)

```bash
make lint        # ruff check
make format      # ruff format
make typecheck   # mypy
make test        # pytest (needs Postgres on :5434, e.g. docker compose up postgres)
```

**Web** (`apps/web`)

```bash
bun run lint
bun run typecheck
bun run build
```

## Pull requests

- Branch off `main` and keep each change focused.
- Follow the conventions in [`apps/api/CONVENTIONS.md`](apps/api/CONVENTIONS.md)
  and [`apps/web/CONVENTIONS.md`](apps/web/CONVENTIONS.md).
- Make sure `ci` (lint, typecheck, tests, build) passes.
- Write a clear description of what changed and why.

## Reporting bugs and security issues

- Bugs and feature requests: open a GitHub issue.
- Security vulnerabilities: follow [`SECURITY.md`](SECURITY.md) and report
  privately, not in a public issue.

## License

By contributing, you agree that your contributions are licensed under the
[Apache License 2.0](LICENSE).
