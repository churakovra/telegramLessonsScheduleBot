from uuid import UUID


class TeacherStudentsNotFound(Exception):
    def __init__(self, teacher_uuid: UUID):
        self.message = f"Teacher {teacher_uuid} has no students"