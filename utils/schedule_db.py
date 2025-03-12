import sqlite3
from datetime import datetime

from utils import datetime_utils
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
