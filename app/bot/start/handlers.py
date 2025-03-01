from aiogram import Router, types, F
from app.bot.menu.keyboards import request_to_support

router = Router()


@router.message(F.text == "/start")
async def start_message_handler(message: types.Message):
    await message.answer(
        text="👋 <b>Welcome</b> to the <b>Telegram Support Bot!</b>\n\n"
             "Need help? Our <b>support team</b> is ready to assist you!\n"
             "Simply create a <code>ticket</code>, and one of our specialists will get in touch with you.\n\n"
             "<b>Press the button</b> below or write /ticket to start a new support request. 🎫",
        reply_markup=request_to_support(),
        parse_mode="HTML"
    )
