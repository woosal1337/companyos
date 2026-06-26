"""customer_requests + link table (COS-140)

Revision ID: d1a5e8c3b472
Revises: c9f4e7b2a361
Create Date: 2026-06-21 09:50:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d1a5e8c3b472"
down_revision: str | None = "c9f4e7b2a361"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customer_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("customer_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), server_default="OPEN", nullable=False),
        sa.Column("source_url", sa.String(length=500), nullable=True),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            name=op.f("fk_customer_requests_org_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name=op.f("fk_customer_requests_customer_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_customer_requests_created_by"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customer_requests")),
    )
    op.create_index("ix_customer_requests_org_id", "customer_requests", ["org_id"])
    op.create_index("ix_customer_requests_customer_id", "customer_requests", ["customer_id"])

    op.create_table(
        "customer_request_tasks",
        sa.Column("request_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["customer_requests.id"],
            name=op.f("fk_customer_request_tasks_request_id"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name=op.f("fk_customer_request_tasks_task_id"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("request_id", "task_id", name=op.f("pk_customer_request_tasks")),
    )


def downgrade() -> None:
    op.drop_table("customer_request_tasks")
    op.drop_index("ix_customer_requests_customer_id", table_name="customer_requests")
    op.drop_index("ix_customer_requests_org_id", table_name="customer_requests")
    op.drop_table("customer_requests")
