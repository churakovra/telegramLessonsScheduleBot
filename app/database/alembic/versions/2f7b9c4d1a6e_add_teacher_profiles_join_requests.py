"""add_teacher_profiles_join_requests

Revision ID: 2f7b9c4d1a6e
Revises: 9c1e7f4a2b33
Create Date: 2026-06-28 04:10:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "2f7b9c4d1a6e"
down_revision: Union[str, Sequence[str], None] = "9c1e7f4a2b33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    join_request_status = sa.Enum(
        "PENDING",
        "APPROVED",
        "REJECTED",
        name="join_request_status",
    )
    join_request_status.create(op.get_bind(), checkfirst=True)

    op.add_column("users", sa.Column("display_name", sa.String(), nullable=True))
    op.add_column("users", sa.Column("bio", sa.String(), nullable=True))
    op.add_column("users", sa.Column("subjects", sa.String(), nullable=True))

    op.create_table(
        "join_requests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.Uuid(), nullable=False),
        sa.Column("student_uuid", sa.Uuid(), nullable=False),
        sa.Column("teacher_uuid", sa.Uuid(), nullable=False),
        sa.Column("status", join_request_status, nullable=False),
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
        sa.ForeignKeyConstraint(["student_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["teacher_uuid"], ["users.uuid"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_uuid",
            "teacher_uuid",
            name="_join_request_student_teacher_uc",
        ),
        sa.UniqueConstraint("uuid"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("join_requests")
    op.drop_column("users", "subjects")
    op.drop_column("users", "bio")
    op.drop_column("users", "display_name")
    sa.Enum(name="join_request_status").drop(op.get_bind(), checkfirst=True)
