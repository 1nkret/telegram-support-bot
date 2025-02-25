from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text="Continue",
                callback_data="menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
