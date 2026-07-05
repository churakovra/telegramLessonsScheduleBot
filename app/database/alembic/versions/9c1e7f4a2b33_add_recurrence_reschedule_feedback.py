"""add_recurrence_reschedule_feedback

Revision ID: 9c1e7f4a2b33
Revises: 5f0c2dfbb6f1
Create Date: 2026-06-28 02:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "9c1e7f4a2b33"
down_revision: Union[str, Sequence[str], None] = "5f0c2dfbb6f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    reschedule_status = postgresql.ENUM(
        "PENDING",
        "APPROVED",
        "REJECTED",
        name="reschedule_status",
        create_type=False,
    )
    reschedule_status.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "slots",
        sa.Column("feedback_prompt_sent_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_table(
        "recurrence_rules",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("teacher_uuid", sa.Uuid(), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("time_start", sa.Time(), nullable=False),
        sa.Column("time_end", sa.Time(), nullable=False),
        sa.Column("slot_duration_minutes", sa.Integer(), nullable=False),
        sa.Column("date_start", sa.Date(), nullable=False),
        sa.Column("date_end", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["teacher_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "reschedule_requests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("slot_uuid", sa.Uuid(), nullable=False),
        sa.Column("student_uuid", sa.Uuid(), nullable=False),
        sa.Column("teacher_uuid", sa.Uuid(), nullable=False),
        sa.Column("requested_date", sa.Date(), nullable=False),
        sa.Column("requested_time", sa.Time(), nullable=False),
        sa.Column("status", reschedule_status, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["slot_uuid"], ["slots.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["teacher_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("slot_uuid", sa.Uuid(), nullable=False),
        sa.Column("student_uuid", sa.Uuid(), nullable=False),
        sa.Column("teacher_uuid", sa.Uuid(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "last_updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["slot_uuid"], ["slots.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["student_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["teacher_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slot_uuid", name="_feedback_slot_uc"),
        sa.UniqueConstraint("uuid"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("feedback")
    op.drop_table("reschedule_requests")
    op.drop_table("recurrence_rules")
    op.drop_column("slots", "feedback_prompt_sent_at")
    sa.Enum(name="reschedule_status").drop(op.get_bind(), checkfirst=True)
