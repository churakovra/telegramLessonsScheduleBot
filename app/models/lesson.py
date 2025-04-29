from datetime import datetime


class Lesson:
    def __init__(self, id_teacher: int, id_student: int, id_lesson_type: int, datetime_start: datetime):
        self.id_teacher = id_teacher
        self.id_student = id_student
        self.id_lesson_type = id_lesson_type
        self.datetime_start = datetime_start
