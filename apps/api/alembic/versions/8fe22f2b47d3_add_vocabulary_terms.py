"""add vocabulary terms

Revision ID: 8fe22f2b47d3
Revises: b9724aff8f44
Create Date: 2026-06-12 02:27:05.294865

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "8fe22f2b47d3"
down_revision: str | None = "b9724aff8f44"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "vocabulary_terms",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("term", sa.String(length=120), nullable=False),
        sa.Column("definition", sa.Text(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_vocabulary_terms_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_vocabulary_terms")),
        sa.UniqueConstraint("org_id", "term", name=op.f("uq_vocabulary_terms_org_id_term")),
    )
    op.create_index(
        op.f("ix_vocabulary_terms_org_id"), "vocabulary_terms", ["org_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_vocabulary_terms_org_id"), table_name="vocabulary_terms")
    op.drop_table("vocabulary_terms")
