from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.crud import get_request


def curator_manage_request_keyboard(request_id: int, curator_id: int):
    data = get_request(request_id)

    status = data[4]
    curator = data[5]

    buttons = []
    row = []

    if status in ["Pending processing", "Curator change"]:
        row.append(
            InlineKeyboardButton(
                text="Take in work",
                callback_data=f"curator_take_request|{request_id}"
            )
        )
        buttons.append(row)
    elif (curator_id == curator and status != "Completed" or
          curator_id == curator and status == "Waiting"):
        row.append(
            InlineKeyboardButton(
                text="Close dialogue",
                callback_data=f"curator_close_request|{request_id}"
            )
        )
        buttons.append(row)

        row = [
            InlineKeyboardButton(
                text="Reassign curator",
                callback_data=f"curator_switch|{request_id}"
            )
        ]
        if status == "In progress":
            row.append(
                InlineKeyboardButton(
                    text="Put on hold",
                    callback_data=f"curator_hold_request|{request_id}"
                )
            )
        elif status == "Waiting":
            row.append(
                InlineKeyboardButton(
                    text="Resume request",
                    callback_data=f"curator_resume_request|{request_id}"
                )
            )
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
