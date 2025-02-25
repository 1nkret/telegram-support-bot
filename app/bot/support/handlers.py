from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.crud import create_request, get_request, update_request_status, add_message, log_action

from .keyboards import create_request_to_support_keyboard, cancel_request_to_support_keyboard, back_to_menu_user
from .state import RequestSupport, Support
from app.utils.find_args import find_args
from app.bot.curator_menu.templates import get_manage_menu
from app.bot.menu.templates import menu_handler_common
from main import bot
from ..curator_menu.keyboards import back_to_curator_menu_keyboard

router = Router()


@router.callback_query(F.data == "request_to_support")
async def request_to_support_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        text="Напишіть повідомлення куратору:",
        reply_markup=create_request_to_support_keyboard()
    )
    await query.answer()
    await state.set_state(RequestSupport.waiting_for_request)


@router.message(RequestSupport.waiting_for_request)
async def request_to_support_create_handler(message: Message, state: FSMContext):
    request_id = create_request(
        request_text=message.text,
        student_id=message.from_user.id
    )
    status = get_request(request_id)[4]
    await message.answer(
        text=f"Запит до куратора було створено. Статус: {status}",
        reply_markup=cancel_request_to_support_keyboard(request_id)
    )
    await state.set_data({"request_id": request_id})
    await state.set_state(RequestSupport.processing_request)


@router.message(RequestSupport.processing_request)
async def text_to_support_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    data_request = get_request(request_id)
    curator_id = data_request[5]
    status = data_request[4]

    if request_id:
        add_message(
            request_id=request_id,
            sender_id=message.from_user.id,
            sender_role="Student",
            message_text=message.text
        )
        if curator_id and status == "В роботі":
            await bot.send_message(
                chat_id=curator_id,
                text=message.text
            )


@router.callback_query(F.data == "back_request_to_support")
async def back_request_to_support_handler(query: CallbackQuery, state: FSMContext):
    await cancel_request(query, state, RequestSupport.waiting_for_request)


@router.callback_query(F.data.startswith("cancel_request_to_support"))
async def cancel_request_to_support_handler(query: CallbackQuery, state: FSMContext):
    canceled = await cancel_request(query, state, RequestSupport.processing_request)
    if canceled:
        return

    request_id = find_args(query.data)[0]
    request_data = get_request(request_id)

    update_request_status(
        request_id=request_id,
        status="Скасовано"
    )

    curator_id = request_data[5]
    if curator_id:
        await bot.send_message(
            chat_id=curator_id,
            text="Студент завершив діалог.",
            reply_markup=back_to_curator_menu_keyboard()
        )


async def cancel_request(query, state, request_state):
    current_state = await state.get_state()
    if current_state == request_state:
        await state.clear()
        await query.message.answer(text="Запит було скасовано.")
        await query.answer()
        return False
    else:
        await query.answer(text="Запит вже скасовано!")
        return True


@router.callback_query(F.data.startswith("curator_take_request"))
async def curator_take_request_callback_handler(query: CallbackQuery, state: FSMContext):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]
    curator_id = data[5]

    if curator_id is not None and curator_id != query.from_user.id:
        await query.answer("Над цим запитом вже працюють!")
        return

    update_request_status(
        request_id=request_id,
        status="В роботі",
        curator_id=query.from_user.id
    )
    log_action(
        request_id=request_id,
        curator_id=query.from_user.id,
        action="Взяв у роботу"
    )
    await get_manage_menu(query)
    await bot.send_message(
        chat_id=user_id,
        text="<b>Куратор на зв`язку!</b>",
        parse_mode="HTML"
    )
    await state.set_state(Support.processing_request)
    await state.set_data({"request_id": request_id})


@router.message(Support.processing_request)
async def curator_send_message_to_request(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    request_data = get_request(request_id)
    student_id = request_data[1]

    add_message(
        message_text=message.text,
        sender_id=message.from_user.id,
        sender_role="Curator",
        request_id=request_id
    )
    await bot.send_message(student_id, f"{message.text}")


@router.callback_query(F.data.startswith("curator_close_request"))
async def curator_close_request_callback_handler(query: CallbackQuery, state: FSMContext):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]
    status = data[4]

    if status not in ["Виконано", "Скасовано"]:
        update_request_status(
            request_id=request_id,
            status="Виконано"
        )
        log_action(
            request_id=request_id,
            curator_id=query.from_user.id,
            action="Закрив запит"
        )
        await get_manage_menu(query)
        await state.clear()
        await bot.send_message(
            chat_id=user_id,
            text="Ваш запит було закрито.",
            reply_markup=back_to_menu_user()
        )
        return
    await query.answer("Запит вже закрито.")


@router.callback_query(F.data.startswith("back_to_menu_user"))
async def curator_close_request_callback_handler(query: CallbackQuery, state: FSMContext):
    st = await state.get_state()

    if st == RequestSupport.processing_request:
        await state.clear()
    await menu_handler_common(query.message)


@router.callback_query(F.data.startswith("curator_switch"))
async def curator_switch_request_callback_handler(query: CallbackQuery):
    await wait_curator_on_request(query, "Зміна куратора")


@router.callback_query(F.data.startswith("curator_hold_request"))
async def curator_hold_request_callback_handler(query: CallbackQuery):
    await wait_curator_on_request(query, "Очікує")


async def wait_curator_on_request(
        query: CallbackQuery,
        status: str
):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]

    update_request_status(
        request_id=request_id,
        status=status,
    )
    log_action(
        request_id=request_id,
        curator_id=query.from_user.id,
        action=f"Змінив статус на \"{status}\""
    )
    await bot.send_message(
        chat_id=user_id,
        text="<b>Куратори зараз не поруч.</b>",
        parse_mode="HTML"
    )
    await get_manage_menu(query)


@router.callback_query(F.data.startswith("curator_resume_request"))
async def curator_resume_request_callback_handler(query: CallbackQuery):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]

    update_request_status(
        request_id=request_id,
        status="В роботі",
    )
    log_action(
        request_id=request_id,
        curator_id=query.from_user.id,
        action="Змінив статус на \"В роботі\""
    )

    await bot.send_message(
        chat_id=user_id,
        text="<b>Куратор на зв`язку!</b>",
        parse_mode="HTML"
    )
    await get_manage_menu(query)
