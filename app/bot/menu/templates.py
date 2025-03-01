from app.bot.menu.keyboards import request_to_support


async def menu_handler_common(target):
    await target.answer(
        text="🎫 <b>Need help?</b> Open a support <b>ticket</b> and get assistance from our team.\n"
             "<b>Press the button</b> below or write /ticket to create a new ticket.",
        reply_markup=request_to_support()
    )
