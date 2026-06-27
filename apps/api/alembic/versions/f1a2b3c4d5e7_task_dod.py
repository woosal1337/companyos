"""task definition-of-done + acceptance criteria

Revision ID: f1a2b3c4d5e7
Revises: e0f1a2b3c4d5
Create Date: 2026-06-19 11:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "f1a2b3c4d5e7"
down_revision: str | None = "e0f1a2b3c4d5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "dod_items",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )
    op.add_column("tasks", sa.Column("acceptance_criteria", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("tasks", "acceptance_criteria")
    op.drop_column("tasks", "dod_items")
