from uuid import UUID


class TeacherStudentsNotFound(Exception):
    def __init__(self, teacher_uuid: UUID):
        self.teacher_uuid = teacher_uuid
        self.message = f"Teacher {teacher_uuid} has no students"

class TeacherAlreadyHasStudentException(Exception):
    def __init__(self, teacher_uuid: UUID, student_uuid: UUID):
        self.teacher_uuid = teacher_uuid,
        self.student_uuid = student_uuid,
        self.message = f"Teacher {teacher_uuid} already has student {student_uuid}"