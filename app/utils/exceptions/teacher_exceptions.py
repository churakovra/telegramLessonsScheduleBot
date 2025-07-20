from uuid import UUID


class TeacherStudentsNotFound(Exception):
    def __init__(self, teacher_uuid: UUID):
        self.message = f"Teacher {teacher_uuid} has no students"

class TeacherAlreadyHasStudentException(Exception):
    def __init__(self, teacher_uuid: UUID, student_uuid: UUID):
        self.message = f"Teacher {teacher_uuid} already has student {student_uuid}"