import sqlite3
from datetime import datetime

import datetime_utils
from lesson import Lesson
from schedule_config import DB_PATH

path = DB_PATH


def set_lesson(lesson: Lesson):
    with sqlite3.connect(database=path) as conn:
        lesson_db = (
            {
                't_username': lesson.t_username,
                's_username': lesson.s_username,
                'lesson_type': lesson.lesson_type,
                'datetime_start': lesson.datetime_start,
                'datetime_end': lesson.datetime_end
            }
        )
        cursor = conn.cursor()
        cursor.execute(
            """
                insert into lessons(t_username, s_username, lesson_type, datetime_start, datetime_end)
                values
	                (:t_username, :s_username, :lesson_type, :datetime_start, :datetime_end);
                """, lesson_db)
        conn.commit()


def get_lessons(day: datetime) -> list[Lesson]:
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
            select * from lessons l
            where l.datetime_start like :datetime_start
            """, day_db)
        for row in execution:
            lessons.append(
                Lesson(
                    t_username=row[1],
                    s_username=row[2],
                    lesson_type=row[3],
                    datetime_start=row[4],
                    datetime_end=row[5])
            )
        conn.commit()
    return lessons
