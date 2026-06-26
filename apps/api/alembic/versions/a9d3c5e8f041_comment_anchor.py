"""comment anchor (inline page comments)

Revision ID: a9d3c5e8f041
Revises: f8c2b4d7e539
Create Date: 2026-06-21 04:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a9d3c5e8f041"
down_revision: str | None = "f8c2b4d7e539"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("comments", sa.Column("anchor", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("comments", "anchor")
