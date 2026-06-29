from aiogram import Router
from aiogram.types import CallbackQuery

from app.keyboard.callback_factories.join_request import (
    StudentJoinRequestCallback,
    StudentTeacherInfoCallback,
)
from app.keyboard.fabric import (
    student_main_menu,
    student_teacher_profile_menu,
    teacher_display_name,
    teacher_subjects_count,
    teacher_subjects_text,
)
from app.message.models import BotMessage
from app.notifier.sender import MessageSender
from app.schemas.user import UserDTO
from app.services.container import Services
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(StudentTeacherInfoCallback.filter())
async def show_teacher_profile(
    callback: CallbackQuery,
    callback_data: StudentTeacherInfoCallback,
    services: Services,
) -> None:
    teacher = await services.teacher.get_teacher_by_uuid(callback_data.teacher_uuid)
    text = BotStrings.Student.TEACHER_PROFILE.format(
        name=teacher_display_name(teacher),
        subjects=teacher_subjects_text(teacher),
        subjects_count=teacher_subjects_count(teacher),
        bio=teacher.bio or "-",
    )
    message = BotMessage(
        text=text,
        markup=student_teacher_profile_menu(teacher_uuid=teacher.uuid),
    )
    await callback.message.answer(**message.to_aiogram_kwargs())
    await callback.answer()


@router.callback_query(StudentJoinRequestCallback.filter())
async def send_join_request(
    callback: CallbackQuery,
    callback_data: StudentJoinRequestCallback,
    services: Services,
    user: UserDTO,
    sender: MessageSender,
) -> None:
    teacher = await services.teacher.get_teacher_by_uuid(callback_data.teacher_uuid)
    try:
        await services.join_request.create_request(
            student_uuid=user.uuid,
            teacher_uuid=teacher.uuid,
        )
    except ValueError:
        await callback.message.answer(
            **BotMessage(
                text=BotStrings.Student.JOIN_REQUEST_ALREADY_EXISTS,
                markup=student_main_menu(),
            ).to_aiogram_kwargs()
        )
        await callback.answer()
        return

    await sender.send_to_chat(
        chat_id=teacher.chat_id,
        text=BotStrings.Teacher.JOIN_REQUEST_CREATED.format(student=user.username),
    )
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Student.JOIN_REQUEST_SENT,
            markup=student_main_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()
