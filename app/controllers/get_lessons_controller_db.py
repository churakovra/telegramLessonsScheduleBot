import sqlite3
from datetime import datetime

from app.utils import datetime_utils
from app.models.lesson import Lesson


def get_lessons(day: datetime, path: str) -> list[Lesson]:
    day_format = day.strftime(datetime_utils.day_format_db)
    day_format = day_format.replace('_', '%')
    day_db = (
        {
            'datetime_start': day_format
        }
    )
    lessons = []
    with sqlite3.connect(database=path) as conn:
        cursor = conn.cursor()
        execution = cursor.execute(
            """
            select t_username, s_username, lesson_type, datetime_start, datetime_end 
            from lessons l
            where l.datetime_start like :datetime_start
            order by datetime_start desc
            """, day_db)
        for row in execution:
            lessons.append(
                Lesson(
                    t_username=row[0],
                    s_username=row[1],
                    lesson_type=row[2],
                    datetime_start=datetime.strptime(row[3], datetime_utils.full_format_no_sec),
                    datetime_end=datetime.strptime(row[4], datetime_utils.full_format_no_sec))
            )
        conn.commit()
    return lessons
