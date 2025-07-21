"""db_initional

Revision ID: c3a6cf94b5c8
Revises: 
Create Date: 2025-07-21 22:34:39.271349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey, DateTime, Uuid, String, Boolean, BigInteger, Integer, UniqueConstraint, text

# revision identifiers, used by Alembic.
revision: str = 'c3a6cf94b5c8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        Column("uuid", Uuid, primary_key=True),
        Column("username", String, unique=True, nullable=False),
        Column("firstname", String, nullable=False),
        Column("lastname", String, nullable=True),
        Column("is_student", Boolean, server_default=text("true")),
        Column("is_teacher", Boolean, server_default=text("false")),
        Column("is_admin", Boolean, server_default=text("false")),
        Column("chat_id", BigInteger, nullable=False),
        Column("dt_reg", DateTime(timezone=True), nullable=False),
        Column("dt_edit", DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "slots",
        Column("uuid", Uuid, primary_key=True),
        Column("uuid_teacher", Uuid, ForeignKey("users.uuid"), nullable=False),
        Column("dt_start", DateTime(timezone=True), nullable=False),
        Column("dt_add", DateTime(timezone=True), nullable=False),
        Column("uuid_student", Uuid, ForeignKey("users.uuid"), nullable=True),
        Column("dt_spot", DateTime(timezone=True), nullable=True),
        UniqueConstraint('uuid_teacher', 'dt_start', name='_teacher_dt_start_uc')
    )

    op.create_table(
        "lessons",
        Column("uuid", Uuid, primary_key=True),
        Column("label", String, nullable=False),
        Column("duration", Integer, nullable=False),
        Column("uuid_teacher", Uuid, ForeignKey("users.uuid"), nullable=False),
        Column("price", Integer, nullable=False)
    )

    op.create_table(
        "teacher_student",
        Column("uuid", Uuid, primary_key=True),
        Column("uuid_teacher", Uuid, ForeignKey("users.uuid")),
        Column("uuid_student", Uuid, ForeignKey("users.uuid")),
        Column("uuid_lesson", Uuid, ForeignKey("lessons.uuid")),
        UniqueConstraint('uuid_teacher', 'uuid_student', name='_teacher_student_uc')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("teacher_student")
    op.drop_table("lessons")
    op.drop_table("slots")
    op.drop_table("users")
