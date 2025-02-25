from app.bot.menu.keyboards import request_to_support


async def menu_handler_common(target):
    await target.answer(
        text="Main menu",
        reply_markup=request_to_support()
    )
