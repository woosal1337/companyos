"""task graph subtasks relations subscriptions bug-kind meeting-link soft-delete

Revision ID: b9724aff8f44
Revises: dd5c4e0ee4f4
Create Date: 2026-06-12 01:54:30.300016

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "b9724aff8f44"
down_revision: str | None = "dd5c4e0ee4f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "project_subscriptions",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("project_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
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
            name=op.f("fk_project_subscriptions_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name=op.f("fk_project_subscriptions_project_id_projects"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_project_subscriptions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_project_subscriptions")),
        sa.UniqueConstraint(
            "project_id", "user_id", name=op.f("uq_project_subscriptions_project_id_user_id")
        ),
    )
    op.create_index(
        op.f("ix_project_subscriptions_org_id"), "project_subscriptions", ["org_id"], unique=False
    )
    op.create_index(
        op.f("ix_project_subscriptions_project_id"),
        "project_subscriptions",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_project_subscriptions_user_id"), "project_subscriptions", ["user_id"], unique=False
    )
    op.create_table(
        "task_relations",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("source_task_id", sa.Uuid(), nullable=False),
        sa.Column("target_task_id", sa.Uuid(), nullable=False),
        sa.Column(
            "type",
            sa.Enum("BLOCKS", "RELATED", name="taskrelationtype", native_enum=False, length=20),
            nullable=False,
        ),
        sa.Column("created_by", sa.Uuid(), nullable=True),
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
            ["created_by"],
            ["users.id"],
            name=op.f("fk_task_relations_created_by_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["organizations.id"],
            name=op.f("fk_task_relations_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["source_task_id"],
            ["tasks.id"],
            name=op.f("fk_task_relations_source_task_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["target_task_id"],
            ["tasks.id"],
            name=op.f("fk_task_relations_target_task_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_relations")),
        sa.UniqueConstraint(
            "source_task_id",
            "target_task_id",
            "type",
            name=op.f("uq_task_relations_source_task_id_target_task_id_type"),
        ),
    )
    op.create_index(op.f("ix_task_relations_org_id"), "task_relations", ["org_id"], unique=False)
    op.create_index(
        op.f("ix_task_relations_source_task_id"), "task_relations", ["source_task_id"], unique=False
    )
    op.create_index(
        op.f("ix_task_relations_target_task_id"), "task_relations", ["target_task_id"], unique=False
    )
    op.create_table(
        "task_subscriptions",
        sa.Column("org_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
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
            name=op.f("fk_task_subscriptions_org_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name=op.f("fk_task_subscriptions_task_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_task_subscriptions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_task_subscriptions")),
        sa.UniqueConstraint(
            "task_id", "user_id", name=op.f("uq_task_subscriptions_task_id_user_id")
        ),
    )
    op.create_index(
        op.f("ix_task_subscriptions_org_id"), "task_subscriptions", ["org_id"], unique=False
    )
    op.create_index(
        op.f("ix_task_subscriptions_task_id"), "task_subscriptions", ["task_id"], unique=False
    )
    op.create_index(
        op.f("ix_task_subscriptions_user_id"), "task_subscriptions", ["user_id"], unique=False
    )
    op.add_column("projects", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("tasks", sa.Column("parent_task_id", sa.Uuid(), nullable=True))
    op.add_column("tasks", sa.Column("source_meeting_id", sa.Uuid(), nullable=True))
    op.add_column(
        "tasks",
        sa.Column(
            "kind",
            sa.Enum("TASK", "BUG", name="taskkind", native_enum=False, length=20),
            nullable=False,
            server_default="TASK",
        ),
    )
    op.add_column(
        "tasks",
        sa.Column(
            "severity",
            sa.Enum(
                "LOW",
                "MEDIUM",
                "HIGH",
                "CRITICAL",
                name="bugseverity",
                native_enum=False,
                length=20,
            ),
            nullable=True,
        ),
    )
    op.add_column("tasks", sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f("ix_tasks_kind"), "tasks", ["kind"], unique=False)
    op.create_index(op.f("ix_tasks_parent_task_id"), "tasks", ["parent_task_id"], unique=False)
    op.create_index(
        op.f("ix_tasks_source_meeting_id"), "tasks", ["source_meeting_id"], unique=False
    )
    op.create_foreign_key(
        op.f("fk_tasks_parent_task_id_tasks"),
        "tasks",
        "tasks",
        ["parent_task_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_tasks_source_meeting_id_meetings"),
        "tasks",
        "meetings",
        ["source_meeting_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("fk_tasks_source_meeting_id_meetings"), "tasks", type_="foreignkey")
    op.drop_constraint(op.f("fk_tasks_parent_task_id_tasks"), "tasks", type_="foreignkey")
    op.drop_index(op.f("ix_tasks_source_meeting_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_parent_task_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_kind"), table_name="tasks")
    op.drop_column("tasks", "archived_at")
    op.drop_column("tasks", "severity")
    op.drop_column("tasks", "kind")
    op.drop_column("tasks", "source_meeting_id")
    op.drop_column("tasks", "parent_task_id")
    op.drop_column("projects", "deleted_at")
    op.drop_index(op.f("ix_task_subscriptions_user_id"), table_name="task_subscriptions")
    op.drop_index(op.f("ix_task_subscriptions_task_id"), table_name="task_subscriptions")
    op.drop_index(op.f("ix_task_subscriptions_org_id"), table_name="task_subscriptions")
    op.drop_table("task_subscriptions")
    op.drop_index(op.f("ix_task_relations_target_task_id"), table_name="task_relations")
    op.drop_index(op.f("ix_task_relations_source_task_id"), table_name="task_relations")
    op.drop_index(op.f("ix_task_relations_org_id"), table_name="task_relations")
    op.drop_table("task_relations")
    op.drop_index(op.f("ix_project_subscriptions_user_id"), table_name="project_subscriptions")
    op.drop_index(op.f("ix_project_subscriptions_project_id"), table_name="project_subscriptions")
    op.drop_index(op.f("ix_project_subscriptions_org_id"), table_name="project_subscriptions")
    op.drop_table("project_subscriptions")
