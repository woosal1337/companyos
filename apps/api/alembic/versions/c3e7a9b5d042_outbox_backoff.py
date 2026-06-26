"""event_outbox.next_attempt_at + failed (poller backoff/DLQ) (COS-274)

Revision ID: c3e7a9b5d042
Revises: b2d6f8c0a931
Create Date: 2026-06-22 14:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c3e7a9b5d042"
down_revision: str | None = "b2d6f8c0a931"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "event_outbox", sa.Column("next_attempt_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "event_outbox", sa.Column("failed", sa.Boolean(), server_default=sa.false(), nullable=False)
    )
    op.create_index(
        "ix_event_outbox_due",
        "event_outbox",
        ["org_id", "delivered_at", "next_attempt_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_event_outbox_due", table_name="event_outbox")
    op.drop_column("event_outbox", "failed")
    op.drop_column("event_outbox", "next_attempt_at")
