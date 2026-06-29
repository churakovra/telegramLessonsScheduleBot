"""fix_critical_db_issues

Revision ID: 79da8cae4485
Revises: bb9743769825
Create Date: 2026-06-27 23:40:41.471963

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '79da8cae4485'
down_revision: Union[str, Sequence[str], None] = 'bb9743769825'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f("lessons_uuid_teacher_fkey"), "lessons", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("lessons_uuid_teacher_fkey"),
        "lessons",
        "users",
        ["uuid_teacher"],
        ["uuid"],
        ondelete="CASCADE",
    )

    op.drop_constraint(op.f("slots_uuid_teacher_fkey"), "slots", type_="foreignkey")
    op.create_foreign_key(
        op.f("slots_uuid_teacher_fkey"),
        "slots",
        "users",
        ["uuid_teacher"],
        ["uuid"],
        ondelete="CASCADE",
    )
    op.drop_constraint(op.f("slots_uuid_student_fkey"), "slots", type_="foreignkey")
    op.create_foreign_key(
        op.f("slots_uuid_student_fkey"),
        "slots",
        "users",
        ["uuid_student"],
        ["uuid"],
        ondelete="CASCADE",
    )

    op.drop_constraint(
        op.f("teacher_student_uuid_teacher_fkey"),
        "teacher_student",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("teacher_student_uuid_teacher_fkey"),
        "teacher_student",
        "users",
        ["uuid_teacher"],
        ["uuid"],
        ondelete="CASCADE",
    )
    op.drop_constraint(
        op.f("teacher_student_uuid_student_fkey"),
        "teacher_student",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("teacher_student_uuid_student_fkey"),
        "teacher_student",
        "users",
        ["uuid_student"],
        ["uuid"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        op.f("teacher_student_uuid_student_fkey"),
        "teacher_student",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("teacher_student_uuid_student_fkey"),
        "teacher_student",
        "users",
        ["uuid_student"],
        ["uuid"],
    )
    op.drop_constraint(
        op.f("teacher_student_uuid_teacher_fkey"),
        "teacher_student",
        type_="foreignkey",
    )
    op.create_foreign_key(
        op.f("teacher_student_uuid_teacher_fkey"),
        "teacher_student",
        "users",
        ["uuid_teacher"],
        ["uuid"],
    )

    op.drop_constraint(op.f("slots_uuid_student_fkey"), "slots", type_="foreignkey")
    op.create_foreign_key(
        op.f("slots_uuid_student_fkey"),
        "slots",
        "users",
        ["uuid_student"],
        ["uuid"],
    )
    op.drop_constraint(op.f("slots_uuid_teacher_fkey"), "slots", type_="foreignkey")
    op.create_foreign_key(
        op.f("slots_uuid_teacher_fkey"),
        "slots",
        "users",
        ["uuid_teacher"],
        ["uuid"],
    )

    op.drop_constraint(
        op.f("lessons_uuid_teacher_fkey"), "lessons", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("lessons_uuid_teacher_fkey"),
        "lessons",
        "users",
        ["uuid_teacher"],
        ["uuid"],
    )
