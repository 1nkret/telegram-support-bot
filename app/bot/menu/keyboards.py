from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def request_to_support():
    buttons = [
        [
            InlineKeyboardButton(
                text="Підтримка",
                callback_data="request_to_support"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
