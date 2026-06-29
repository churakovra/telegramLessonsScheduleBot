from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboard.callback_factories.feedback import (
    FeedbackCallback,
    FeedbackCommentCallback,
)
from app.keyboard.fabric import feedback_comment_menu, student_main_menu
from app.message.models import BotMessage
from app.schemas.user import UserDTO
from app.services.container import Services
from app.states.schedule_states import ScheduleStates
from app.utils.bot_strings import BotStrings

router = Router()


@router.callback_query(FeedbackCallback.filter())
async def handle_feedback_rating(
    callback: CallbackQuery,
    callback_data: FeedbackCallback,
) -> None:
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Student.FEEDBACK_COMMENT_QUESTION,
            markup=feedback_comment_menu(
                slot_uuid=callback_data.slot_uuid,
                rating=callback_data.rating,
            ),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.callback_query(FeedbackCommentCallback.filter())
async def handle_feedback_comment_choice(
    callback: CallbackQuery,
    callback_data: FeedbackCommentCallback,
    state: FSMContext,
    services: Services,
    user: UserDTO,
) -> None:
    if callback_data.add_comment:
        await state.update_data(
            feedback_slot_uuid=callback_data.slot_uuid,
            feedback_rating=callback_data.rating,
        )
        await state.set_state(ScheduleStates.wait_for_feedback_comment)
        await callback.message.answer(
            **BotMessage(text=BotStrings.Student.FEEDBACK_COMMENT).to_aiogram_kwargs()
        )
        await callback.answer()
        return

    await services.feedback.submit_feedback(
        slot_uuid=callback_data.slot_uuid,
        student_uuid=user.uuid,
        rating=callback_data.rating,
        comment=None,
    )
    await callback.message.answer(
        **BotMessage(
            text=BotStrings.Student.FEEDBACK_THANKS,
            markup=student_main_menu(),
        ).to_aiogram_kwargs()
    )
    await callback.answer()


@router.message(ScheduleStates.wait_for_feedback_comment)
async def wait_for_feedback_comment(
    message: Message,
    state: FSMContext,
    services: Services,
    user: UserDTO,
) -> None:
    data = await state.get_data()
    await services.feedback.submit_feedback(
        slot_uuid=data["feedback_slot_uuid"],
        student_uuid=user.uuid,
        rating=data["feedback_rating"],
        comment=message.text,
    )
    await state.clear()
    await message.answer(
        **BotMessage(
            text=BotStrings.Student.FEEDBACK_THANKS,
            markup=student_main_menu(),
        ).to_aiogram_kwargs()
    )
