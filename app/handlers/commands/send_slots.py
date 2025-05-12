from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(Command("send_slots"))
async def send_slots(stage: FSMContext):
    data = await stage.get_data()
    slots = data.get("slots")