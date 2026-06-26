"""type-specific workflow transitions (kind column) (COS-202)

Revision ID: f3c7b2e9a648
Revises: e2b6c9d4a583
Create Date: 2026-06-21 10:55:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f3c7b2e9a648"
down_revision: str | None = "e2b6c9d4a583"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("workflow_transitions", sa.Column("kind", sa.String(length=20), nullable=True))
    op.drop_constraint(
        "uq_workflow_transitions_org_id_from_status_id_to_status_id",
        "workflow_transitions",
        type_="unique",
    )
    op.create_index(
        "uq_workflow_transitions_rule",
        "workflow_transitions",
        ["org_id", "from_status_id", "to_status_id", "kind"],
        unique=True,
        postgresql_nulls_not_distinct=True,
    )


def downgrade() -> None:
    op.drop_index("uq_workflow_transitions_rule", table_name="workflow_transitions")
    op.create_unique_constraint(
        "uq_workflow_transitions_org_id_from_status_id_to_status_id",
        "workflow_transitions",
        ["org_id", "from_status_id", "to_status_id"],
    )
    op.drop_column("workflow_transitions", "kind")
