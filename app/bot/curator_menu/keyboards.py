from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.get_datetime import get_datetime
from database.crud import get_active_requests, get_request, get_closed_requests

PAGE_SIZE = 6


def create_pagination_buttons(requests, page, total_pages, callback_prefix, add_button=None):
    buttons = []
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    row = []

    for el in requests[start:end]:
        formatted_date = get_datetime(el[3])
        row.append(InlineKeyboardButton(
            text=f"{el[0]} | {formatted_date}",
            callback_data=f"curator_get_request|{el[0]}"
        ))

        if len(row) == 2:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Prev",
                callback_data=f"{callback_prefix}_page|{page - 1}"
            )
        )
    if add_button:
        nav_buttons.append(add_button)
    if page < total_pages - 1:
        nav_buttons.append(
            InlineKeyboardButton(
                text="Next", callback_data=f"{callback_prefix}_page|{page + 1}"
            )
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def curator_menu_keyboard(page=0):
    requests = get_active_requests()
    total_pages = (len(requests) + PAGE_SIZE - 1) // PAGE_SIZE
    return create_pagination_buttons(
        requests,
        page,
        total_pages,
        "curator_get_paginator_request",
        InlineKeyboardButton(
            text="History",
            callback_data="get_history_requests"
        )
    )


def curator_menu_closed_requests_keyboard(page=0):
    requests = get_closed_requests()
    total_pages = (len(requests) + PAGE_SIZE - 1) // PAGE_SIZE
    return create_pagination_buttons(
        requests,
        page,
        total_pages,
        "curator_get_closed_request",
        InlineKeyboardButton(
            text="Back",
            callback_data="curator_menu"
        )
    )


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
    buttons.append(
        [
            InlineKeyboardButton(
                text="Повернутися",
                callback_data="curator_menu"
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_curator_menu_keyboard():
    buttons = [
        [
            InlineKeyboardButton(
                text="Повернутися",
                callback_data="curator_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
