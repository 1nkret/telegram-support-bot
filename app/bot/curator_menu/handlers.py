from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from .keyboards import curator_menu_keyboard, curator_menu_closed_requests_keyboard
from .templates import get_manage_menu

router = Router()


@router.message(F.text == "/curator")
async def curator_menu_handler(message: Message):
    await curator_get_menu(message)


@router.callback_query(F.data == "curator_menu")
async def curator_menu_callback_handler(query: CallbackQuery):
    await curator_get_menu(query.message)


async def curator_get_menu(message: Message):
    await message.answer(
        text="Curator menu",
        reply_markup=curator_menu_keyboard()
    )


@router.callback_query(F.data.startswith("curator_get_request"))
async def curator_take_request_callback_handler(query: CallbackQuery):
    await get_manage_menu(query)


@router.callback_query(F.data == "get_history_requests")
async def curator_history_callback_handler(query: CallbackQuery):
    await query.message.answer(
        text="Curator history",
        reply_markup=curator_menu_closed_requests_keyboard()
    )


@router.callback_query(F.data.startswith("curator_get_paginator_request_page"))
async def paginate_active_requests(query: CallbackQuery):
    page = query.data.split("|")[-1]
    page = int(page)
    await query.message.edit_reply_markup(
        reply_markup=curator_menu_keyboard(page)
    )


@router.callback_query(F.data.startswith("curator_get_closed_request_page"))
async def paginate_closed_requests(query: CallbackQuery):
    page = query.data.split("|")[-1]
    page = int(page)
    await query.message.edit_reply_markup(
        reply_markup=curator_menu_closed_requests_keyboard(page)
    )
