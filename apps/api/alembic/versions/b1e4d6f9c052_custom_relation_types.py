"""custom relation types (RelationTypeDef + task_relations.custom_type_id)

Revision ID: b1e4d6f9c052
Revises: a9d3c5e8f041
Create Date: 2026-06-21 05:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b1e4d6f9c052"
down_revision: str | None = "a9d3c5e8f041"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "relation_type_defs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=60), nullable=False),
        sa.Column("outward_label", sa.String(length=60), nullable=False),
        sa.Column("inward_label", sa.String(length=60), nullable=False),
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
            name=op.f("fk_relation_type_defs_org_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_relation_type_defs")),
        sa.UniqueConstraint("org_id", "name", name=op.f("uq_relation_type_defs_org_name")),
    )
    op.create_index("ix_relation_type_defs_org_id", "relation_type_defs", ["org_id"])

    op.add_column("task_relations", sa.Column("custom_type_id", sa.Uuid(), nullable=True))
    op.create_index("ix_task_relations_custom_type_id", "task_relations", ["custom_type_id"])
    op.create_foreign_key(
        op.f("fk_task_relations_custom_type_id"),
        "task_relations",
        "relation_type_defs",
        ["custom_type_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        "uq_task_relations_source_task_id_target_task_id_type", "task_relations", type_="unique"
    )
    op.create_index(
        "uq_task_relations_pair",
        "task_relations",
        ["source_task_id", "target_task_id", "type", "custom_type_id"],
        unique=True,
        postgresql_nulls_not_distinct=True,
    )


def downgrade() -> None:
    op.drop_index("uq_task_relations_pair", table_name="task_relations")
    op.create_unique_constraint(
        "uq_task_relations_source_task_id_target_task_id_type",
        "task_relations",
        ["source_task_id", "target_task_id", "type"],
    )
    op.drop_constraint(
        op.f("fk_task_relations_custom_type_id"), "task_relations", type_="foreignkey"
    )
    op.drop_index("ix_task_relations_custom_type_id", table_name="task_relations")
    op.drop_column("task_relations", "custom_type_id")
    op.drop_index("ix_relation_type_defs_org_id", table_name="relation_type_defs")
    op.drop_table("relation_type_defs")
