from sqlalchemy.util import await_only

from app.repositories.teacher_repo import TeacherRepo
from app.services.teacher_service import TeacherService


async def attach_student_to_teacher_use_case(teacher: str, student: str) -> bool:
    if not await TeacherService.check_user_exists(teacher):
        return False
    if not await TeacherService.check_user_status(teacher):
        return False
    return await TeacherRepo.attach_student(teacher, student)
