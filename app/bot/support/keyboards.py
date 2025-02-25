from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_request_to_support_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text="Повернутися",
                callback_data="back_request_to_support"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_request_to_support_keyboard(request_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Завершити діалог",
                callback_data=f"cancel_request_to_support|{request_id},"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_user():
    buttons = [
        [
            InlineKeyboardButton(
                text="Повернутися до меню",
                callback_data="back_to_menu_user"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
