from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.slot_repository import SlotRepository
from app.repositories.user_repository import UserRepository
from app.utils.bot_strings import BotStrings
from app.utils.enums.bot_values import StatisticsPeriod


@dataclass(frozen=True)
class TeacherStats:
    total_lessons: int
    total_hours: float
    total_earnings: int
    lessons_per_student: dict[str, int]
    most_popular_lesson_type: str | None


@dataclass(frozen=True)
class StudentStats:
    total_lessons: int
    total_hours: float
    teachers: list[str]
    upcoming_lessons_count: int


@dataclass(frozen=True)
class AdminStats:
    total_users: int
    total_teachers: int
    total_students: int
    active_teachers_this_week: int
    total_lessons_this_week: int


class StatisticsService:
    def __init__(
        self,
        session: AsyncSession | None = None,
        slot_repository: SlotRepository | None = None,
        user_repository: UserRepository | None = None,
    ):
        if slot_repository is None:
            if session is None:
                raise ValueError("StatisticsService requires session or slot_repository")
            slot_repository = SlotRepository(session)
        if user_repository is None and session is not None:
            user_repository = UserRepository(session)
        self._slot_repository = slot_repository
        self._user_repository = user_repository

    async def get_teacher_stats(
        self, teacher_uuid: UUID, period: StatisticsPeriod
    ) -> TeacherStats:
        start_at, end_at = self._period_bounds(period)
        rows = await self._slot_repository.get_booked_slots_for_stats(
            teacher_uuid, start_at, end_at, as_teacher=True
        )

        lessons_per_student: Counter[str] = Counter()
        lesson_types: Counter[str] = Counter()
        total_minutes = 0
        total_earnings = 0

        for _slot, _teacher, student, lesson in rows:
            student_name = " ".join(
                part for part in [student.firstname, student.lastname] if part
            )
            lessons_per_student[student_name or student.username] += 1
            if lesson is None:
                continue
            total_minutes += lesson.duration
            total_earnings += lesson.price
            lesson_types[lesson.label] += 1

        return TeacherStats(
            total_lessons=len(rows),
            total_hours=round(total_minutes / 60, 2),
            total_earnings=total_earnings,
            lessons_per_student=dict(lessons_per_student),
            most_popular_lesson_type=lesson_types.most_common(1)[0][0]
            if lesson_types
            else None,
        )

    async def get_student_stats(
        self, student_uuid: UUID, period: StatisticsPeriod
    ) -> StudentStats:
        start_at, end_at = self._period_bounds(period)
        rows = await self._slot_repository.get_booked_slots_for_stats(
            student_uuid, start_at, end_at, as_teacher=False
        )
        upcoming = await self._slot_repository.get_student_booked_slots(
            student_uuid, datetime.now(UTC).astimezone(), end_at
        )

        teachers = {
            " ".join(part for part in [teacher.firstname, teacher.lastname] if part)
            or teacher.username
            for _slot, teacher, _student, _lesson in rows
        }
        total_minutes = sum(lesson.duration for *_rest, lesson in rows if lesson)

        return StudentStats(
            total_lessons=len(rows),
            total_hours=round(total_minutes / 60, 2),
            teachers=sorted(teachers),
            upcoming_lessons_count=len(upcoming),
        )

    async def get_weekly_summary(self, student_uuid: UUID) -> str:
        now = datetime.now(UTC).astimezone()
        start_at = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_at = start_at + timedelta(days=7)
        rows = await self._slot_repository.get_booked_slots_for_stats(
            student_uuid, start_at, end_at, as_teacher=False
        )
        if not rows:
            return BotStrings.Student.WEEKLY_SCHEDULE_EMPTY

        lines = [BotStrings.Student.WEEKLY_SCHEDULE_TITLE]
        current_day = None
        total_minutes = 0
        for slot, teacher, _student, lesson in rows:
            lesson_day = slot.dt_start.date()
            if lesson_day != current_day:
                current_day = lesson_day
                lines.extend(
                    [
                        "",
                        BotStrings.Student.WEEKLY_SCHEDULE_DAY.format(
                            weekday=BotStrings.Common.WEEKDAY_SHORT_LABELS[
                                slot.dt_start.weekday()
                            ],
                            date=slot.dt_start.strftime("%d.%m"),
                        ),
                    ]
                )

            lesson_label = lesson.label if lesson else "-"
            teacher_name = (
                " ".join(part for part in [teacher.firstname, teacher.lastname] if part)
                or teacher.username
            )
            if lesson:
                total_minutes += lesson.duration
            lines.append(
                BotStrings.Student.WEEKLY_SCHEDULE_ITEM.format(
                    time=slot.dt_start.strftime("%H:%M"),
                    lesson=lesson_label,
                    teacher=teacher_name,
                )
            )

        total_hours = round(total_minutes / 60, 2)
        lines.extend(
            [
                "",
                BotStrings.Student.WEEKLY_SCHEDULE_TOTAL.format(
                    count=len(rows),
                    hours=f"{total_hours:g}",
                ),
            ]
        )
        return "\n".join(lines)

    async def get_admin_stats(self) -> AdminStats:
        if self._user_repository is None:
            raise ValueError("StatisticsService requires user_repository")

        start_at, end_at = self._period_bounds(StatisticsPeriod.WEEK)
        total_users, total_teachers, total_students = (
            await self._user_repository.get_admin_counts()
        )
        total_lessons, active_teachers = await self._slot_repository.get_admin_week_stats(
            start_at, end_at
        )
        return AdminStats(
            total_users=total_users,
            total_teachers=total_teachers,
            total_students=total_students,
            active_teachers_this_week=active_teachers,
            total_lessons_this_week=total_lessons,
        )

    @staticmethod
    def _period_bounds(period: StatisticsPeriod) -> tuple[datetime, datetime]:
        now = datetime.now(UTC).astimezone()
        if period == StatisticsPeriod.WEEK:
            start_at = (now - timedelta(days=now.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            end_at = start_at + timedelta(days=7)
            return start_at, end_at
        if period == StatisticsPeriod.MONTH:
            start_at = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if start_at.month == 12:
                end_at = start_at.replace(year=start_at.year + 1, month=1)
            else:
                end_at = start_at.replace(month=start_at.month + 1)
            return start_at, end_at

        start_at = now.replace(
            month=1, day=1, hour=0, minute=0, second=0, microsecond=0
        )
        end_at = start_at.replace(year=start_at.year + 1)
        return start_at, end_at
