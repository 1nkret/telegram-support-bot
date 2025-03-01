from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from core.config import FORUM_CHAT_ID
from database.crud import create_request, get_request, update_request_status, add_message, log_action, update_thread_id

from .keyboards import create_request_to_support_keyboard, cancel_request_to_support_keyboard, back_to_menu_user
from .state import RequestSupport, Support

from app.utils.find_args import find_args
from app.utils.get_datetime import get_datetime
from app.bot.support_menu.templates import get_manage_menu
from main import bot

router = Router()


@router.callback_query(F.data == "request_to_support")
async def request_to_support_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        text="Write your message to support:",
        reply_markup=create_request_to_support_keyboard()
    )
    await query.answer()
    await state.set_state(RequestSupport.waiting_for_request)


@router.message(RequestSupport.waiting_for_request)
async def request_to_support_create_handler(message: Message, state: FSMContext):
    request_id = create_request(
        request_text=message.text,
        user_id=message.from_user.id
    )
    data = get_request(request_id)
    status = data[4]

    name = f"{data[0]} | {get_datetime(data[3])}"

    action = await bot.create_forum_topic(
        chat_id=FORUM_CHAT_ID,
        name=name
    )
    update_thread_id(request_id, action.message_thread_id)

    await state.set_data({"request_id": request_id})
    await state.set_state(RequestSupport.processing_request)

    text, kb = await get_manage_menu(request_id, None)

    await bot.send_message(
        chat_id=FORUM_CHAT_ID,
        message_thread_id=action.message_thread_id,
        text=text,
        reply_markup=kb,
        parse_mode="HTML"
    )
    await message.answer(
        text=f"Request to support was created. Status: {status}",
        reply_markup=cancel_request_to_support_keyboard(request_id)
    )


@router.message(RequestSupport.processing_request)
async def text_to_support_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    data = get_request(request_id)

    thread_id = data[7]

    if request_id:
        add_message(
            request_id=request_id,
            sender_id=message.from_user.id,
            sender_role="User",
            message_text=message.text
        )
        await bot.send_message(
            chat_id=FORUM_CHAT_ID,
            text=message.text,
            message_thread_id=thread_id
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
    data = get_request(request_id)

    update_request_status(
        request_id=request_id,
        status="Cancelled"
    )

    thread_id = data[7]

    await bot.send_message(
        chat_id=FORUM_CHAT_ID,
        text="<b>The user has closed the dialogue.</b>",
        message_thread_id=thread_id,
        parse_mode="HTML"
    )


async def cancel_request(query, state, request_state):
    current_state = await state.get_state()
    if current_state == request_state:
        await state.clear()
        await query.message.answer(text="Request was cancelled.")
        await query.answer()
        return False
    else:
        await query.answer(text="Request is already cancelled!")
        return True


@router.callback_query(F.data.startswith("support_take_request"))
async def support_take_request_callback_handler(query: CallbackQuery, state: FSMContext):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]
    support_id = data[5]

    if support_id is not None and support_id != query.from_user.id:
        await query.answer("Someone is already working on this request!")
        return

    update_request_status(
        request_id=request_id,
        status="In progress",
        support_id=query.from_user.id
    )
    log_action(
        request_id=request_id,
        support_id=query.from_user.id,
        action="Started working on the request"
    )

    text, kb = await get_manage_menu(request_id, query.from_user.id)
    await query.message.edit_text(
        text=text,
        reply_markup=kb,
        parse_mode="HTML"
    )
    await bot.send_message(
        chat_id=user_id,
        text="<b>Support is in touch!</b>",
        parse_mode="HTML"
    )
    await state.set_state(Support.processing_request)
    await state.set_data({"request_id": request_id})


@router.message(Support.processing_request)
async def support_send_message_to_request(message: Message, state: FSMContext):
    data = await state.get_data()
    request_id = data.get("request_id")
    request_data = get_request(request_id)
    user_id = request_data[1]

    add_message(
        message_text=message.text,
        sender_id=message.from_user.id,
        sender_role="Support",
        request_id=request_id
    )
    await bot.send_message(user_id, f"{message.text}")


@router.callback_query(F.data.startswith("support_close_request"))
async def support_close_request_callback_handler(query: CallbackQuery, state: FSMContext):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]
    status = data[4]
    support_id = data[6]

    if status not in ["Completed", "Cancelled"]:
        update_request_status(
            request_id=request_id,
            status="Completed"
        )
        log_action(
            request_id=request_id,
            support_id=query.from_user.id,
            action="Closed the request"
        )

        text, kb = await get_manage_menu(request_id, support_id)
        await query.message.edit_text(
            text=text,
            reply_markup=kb,
            parse_mode="HTML"
        )
        await bot.send_message(
            chat_id=user_id,
            text="Your request has been closed.",
            reply_markup=back_to_menu_user()
        )
        await state.clear()
        return
    await query.answer("Request is already closed.")


@router.callback_query(F.data.startswith("support_switch"))
async def support_switch_request_callback_handler(query: CallbackQuery, state: FSMContext):
    await wait_support_on_request(
        query=query,
        status="Support change",
        state=state,
    )


@router.callback_query(F.data.startswith("support_hold_request"))
async def support_hold_request_callback_handler(query: CallbackQuery, state: FSMContext):
    await wait_support_on_request(
        query=query,
        status="Waiting",
        state=state,
    )


async def wait_support_on_request(
        query: CallbackQuery,
        status: str,
        state: FSMContext,
):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]

    current_state = await state.get_state()
    if current_state == Support.processing_request:
        await state.clear()

    update_request_status(
        request_id=request_id,
        status=status,
    )

    log_action(
        request_id=request_id,
        support_id=query.from_user.id,
        action=f"Changed status to \"{status}\""
    )
    await bot.send_message(
        chat_id=user_id,
        text="<b>Support is currently unavailable.</b>",
        parse_mode="HTML"
    )

    text, kb, = await get_manage_menu(request_id, query.from_user.id)
    await query.message.edit_text(
        text=text,
        reply_markup=kb,
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("support_resume_request"))
async def support_resume_request_callback_handler(query: CallbackQuery, state: FSMContext):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    user_id = data[1]

    update_request_status(
        request_id=request_id,
        status="In progress",
    )
    log_action(
        request_id=request_id,
        support_id=query.from_user.id,
        action="Changed status to \"In progress\""
    )

    await bot.send_message(
        chat_id=user_id,
        text="<b>Support is now available!</b>",
        parse_mode="HTML"
    )
