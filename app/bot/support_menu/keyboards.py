from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.crud import get_request


def support_manage_request_keyboard(request_id: int, support_id: int):
    data = get_request(request_id)

    status = data[4]
    support = data[5]

    buttons = []
    row = []

    if status in ["Pending processing", "Support change"]:
        row.append(
            InlineKeyboardButton(
                text="Take in work",
                callback_data=f"support_take_request|{request_id}"
            )
        )
        buttons.append(row)
    elif (support_id == support and status != "Completed" or
          support_id == support and status == "Waiting"):
        row.append(
            InlineKeyboardButton(
                text="Close dialogue",
                callback_data=f"support_close_request|{request_id}"
            )
        )
        buttons.append(row)

        row = [
            InlineKeyboardButton(
                text="Reassign support",
                callback_data=f"support_switch|{request_id}"
            )
        ]
        if status == "In progress":
            row.append(
                InlineKeyboardButton(
                    text="Put on hold",
                    callback_data=f"support_hold_request|{request_id}"
                )
            )
        elif status == "Waiting":
            row.append(
                InlineKeyboardButton(
                    text="Resume request",
                    callback_data=f"support_resume_request|{request_id}"
                )
            )
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
