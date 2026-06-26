"""webhook signing secret (HMAC)

Revision ID: b0c1d2e3f4a5
Revises: a9b0c1d2e3f4
Create Date: 2026-06-20 09:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b0c1d2e3f4a5"
down_revision: str | None = "a9b0c1d2e3f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("project_webhooks", sa.Column("secret", sa.String(length=64), nullable=True))
    op.execute(
        "UPDATE project_webhooks SET secret = md5(random()::text || id::text) WHERE secret IS NULL"
    )
    op.alter_column("project_webhooks", "secret", nullable=False)


def downgrade() -> None:
    op.drop_column("project_webhooks", "secret")
