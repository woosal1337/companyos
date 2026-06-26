"""workflow transition required_role (role-gated transitions)

Revision ID: c5d6e7f8a9b0
Revises: b4c5d6e7f8a9
Create Date: 2026-06-20 17:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c5d6e7f8a9b0"
down_revision: str | None = "b4c5d6e7f8a9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "workflow_transitions",
        sa.Column("required_role", sa.String(length=20), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("workflow_transitions", "required_role")
