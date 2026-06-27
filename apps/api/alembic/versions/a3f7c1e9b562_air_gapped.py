"""instance_settings.air_gapped (COS-216)

Revision ID: a3f7c1e9b562
Revises: f8a2c6e0b449
Create Date: 2026-06-22 19:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a3f7c1e9b562"
down_revision: str | None = "f8a2c6e0b449"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "instance_settings",
        sa.Column("air_gapped", sa.Boolean(), server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("instance_settings", "air_gapped")
