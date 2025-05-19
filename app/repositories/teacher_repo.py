from app.database import SessionLocal
from app.models.orm.teacher_students import TeacherStudents
from app.models.user_dto import UserDTO


class TeacherRepo:
    @staticmethod
    async def attach_student(teacher: str, student: str) -> bool:
        try:
            with SessionLocal.begin() as session:
                teacher_student = TeacherStudents(teacher_username=teacher, student_username=student)
                session.add(teacher_student)
        except Exception:
            return False
        return True
