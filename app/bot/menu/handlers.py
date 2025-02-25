from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from .templates import menu_handler_common

router = Router()


@router.message(F.text == "/menu")
async def menu_message_handler(message: Message):
    await menu_handler_common(message)


@router.callback_query(F.data == "menu")
async def menu_callback_handler(query: CallbackQuery):
    await menu_handler_common(query.message)
    await query.answer()
