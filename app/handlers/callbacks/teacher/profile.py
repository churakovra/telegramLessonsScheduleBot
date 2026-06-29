from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboard.callback_factories.profile import TeacherProfileCallback
from app.keyboard.fabric import (
    cancel_markup,
    teacher_main_menu,
    teacher_profile_menu,
    teacher_subjects_text,
)
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(TeacherProfileCallback.filter())
async def show_or_edit_profile(
    callback: CallbackQuery,
    callback_data: TeacherProfileCallback,
    services: Services,
    user: UserDTO,
    state: FSMContext,
) -> None:
    teacher = await services.teacher.get_teacher_by_uuid(user.uuid)
    if not callback_data.edit:
        await callback.message.answer(
            **BotMessage(
                text=_profile_text(teacher),
                markup=teacher_profile_menu(),
            ).to_aiogram_kwargs()
        )
        await callback.answer()
        return

    await state.clear()
    await state.update_data(
        display_name=teacher.display_name,
        bio=teacher.bio,
        subjects=teacher.subjects,
        teacher_uuid=teacher.uuid,
    )
    await state.set_state(ScheduleStates.wait_for_teacher_profile_display_name)
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Teacher.PROFILE_DISPLAY_NAME,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.message(ScheduleStates.wait_for_teacher_profile_display_name)
async def wait_for_display_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(
        display_name=_profile_value(message.text, data.get("display_name"))
    )
    await state.set_state(ScheduleStates.wait_for_teacher_profile_bio)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.PROFILE_BIO,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_teacher_profile_bio)
async def wait_for_bio(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.update_data(bio=_profile_value(message.text, data.get("bio")))
    await state.set_state(ScheduleStates.wait_for_teacher_profile_subjects)
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.PROFILE_SUBJECTS,
            markup=cancel_markup(),
        ).to_aiogram_kwargs()
    )


@router.message(ScheduleStates.wait_for_teacher_profile_subjects)
async def wait_for_subjects(
    message: Message,
    state: FSMContext,
    services: Services,
) -> None:
    data = await state.get_data()
    subjects = _profile_value(message.text, data.get("subjects"))
    await services.teacher.update_profile(
        data["teacher_uuid"],
        display_name=data.get("display_name"),
        bio=data.get("bio"),
        subjects=subjects,
    )
    await state.clear()
    await message.answer(
        **BotMessage(
            text=BotStrings.Teacher.PROFILE_SAVED,
            markup=teacher_main_menu(),
        ).to_aiogram_kwargs()
    )


def _profile_text(teacher: UserDTO) -> str:
    return BotStrings.Teacher.PROFILE.format(
        display_name=teacher.display_name or "-",
        subjects=teacher_subjects_text(teacher),
        bio=teacher.bio or "-",
    )


def _profile_value(value: str | None, current: str | None) -> str | None:
    if value is None:
        return current
    normalized = value.strip()
    if normalized == "-":
        return current
    return normalized or current
