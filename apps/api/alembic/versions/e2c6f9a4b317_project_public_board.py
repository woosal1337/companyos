"""projects.public_token + public_attributes (COS-249)

Revision ID: e2c6f9a4b317
Revises: d1b5f8c4a296
Create Date: 2026-06-22 09:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "e2c6f9a4b317"
down_revision: str | None = "d1b5f8c4a296"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("public_token", sa.String(length=64), nullable=True))
    op.add_column(
        "projects",
        sa.Column(
            "public_attributes",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'[]'::jsonb"),
            nullable=False,
        ),
    )
    op.create_index("ix_projects_public_token", "projects", ["public_token"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_projects_public_token", table_name="projects")
    op.drop_column("projects", "public_attributes")
    op.drop_column("projects", "public_token")
