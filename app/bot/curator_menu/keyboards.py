from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.crud import get_request

PAGE_SIZE = 6


def curator_manage_request_keyboard(request_id: int, curator_id: int):
    data = get_request(request_id)

    status = data[4]
    curator = data[5]

    buttons = []
    row = []

    if status in ["Ожидает обработки", "Зміна куратора"]:
        row.append(
            InlineKeyboardButton(
                text="Взяти в роботу",
                callback_data=f"curator_take_request|{request_id}"
            )
        )
        buttons.append(row)
    elif (curator_id == curator and status != "Виконано" or
          curator_id == curator and status == "Очікує"):
        row.append(
            InlineKeyboardButton(
                text="Завершити діалог",
                callback_data=f"curator_close_request|{request_id}"
            )
        )
        buttons.append(row)

        row = [
            InlineKeyboardButton(
                text="Переназначити куратора",
                callback_data=f"curator_switch|{request_id}"
            )
        ]
        if status == "В роботі":
            row.append(
                InlineKeyboardButton(
                    text="Поставити на утримання",
                    callback_data=f"curator_hold_request|{request_id}"
                )
            )
        elif status == "Очікує":
            row.append(
                InlineKeyboardButton(
                    text="Зняти з утримання",
                    callback_data=f"curator_resume_request|{request_id}"
                )
            )
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
