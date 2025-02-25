from aiogram import Router, types, F
from .keyboards import start_keyboard

router = Router()


@router.message(F.text == "/start")
async def start_message_handler(message: types.Message):
    await message.answer(
        text="Start message. Push button to continue",
        reply_markup=start_keyboard()
    )
