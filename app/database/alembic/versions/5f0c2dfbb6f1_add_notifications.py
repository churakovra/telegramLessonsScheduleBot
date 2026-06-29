"""add_notifications

Revision ID: 5f0c2dfbb6f1
Revises: 79da8cae4485
Create Date: 2026-06-28 01:40:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "5f0c2dfbb6f1"
down_revision: Union[str, Sequence[str], None] = "79da8cae4485"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    trigger_type = sa.Enum(
        "BEFORE_LESSON",
        "CUSTOM",
        name="notification_trigger_type",
    )
    trigger_type.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("teacher_uuid", sa.Uuid(), nullable=False),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("trigger_type", trigger_type, nullable=False),
        sa.Column("minutes_before", sa.Integer(), nullable=False),
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


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("notifications")
    sa.Enum(name="notification_trigger_type").drop(op.get_bind(), checkfirst=True)
