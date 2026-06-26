"""meeting summary structured lines

Revision ID: 1fa178a681a1
Revises: a58ad0c1c190
Create Date: 2026-06-14 11:38:01.817360

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "1fa178a681a1"
down_revision: str | None = "a58ad0c1c190"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "meeting_summaries",
        sa.Column("summary_lines", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("meeting_summaries", "summary_lines")
