import sqlite3

from app.utils import datetime_utils
from app.models.lesson import Lesson


def set_lesson(lesson: Lesson, path: str):
    with sqlite3.connect(database=path) as conn:
        lesson_db = (
            {
                't_username': lesson.t_username,
                's_username': lesson.s_username,
                'lesson_type': lesson.lesson_type,
                'datetime_start': lesson.datetime_start.strftime(datetime_utils.full_format_no_sec),
                'datetime_end': lesson.datetime_end.strftime(datetime_utils.full_format_no_sec)
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