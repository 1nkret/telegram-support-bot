from app.bot.curator_menu.keyboards import curator_manage_request_keyboard
from app.utils.find_args import find_args
from app.utils.get_datetime import get_datetime, get_short_datetime
from database.crud import get_request, get_messages


async def get_manage_menu(query, msg: str = ""):
    request_id = find_args(query.data)[0]
    data = get_request(request_id)
    print(request_id, data)
    if data is None:
        await query.message.edit_text(
            "❌ Ошибка: Запрос не найден.",
            parse_mode="HTML"
        )
        return

    data_messages = get_messages(request_id)

    request_text = data[2]
    created_at = data[3]
    status = data[4]
    taken_at = data[6]

    if taken_at:
        taken_at = (f"<b>Час взяття запиту:</b> <code>{get_datetime(taken_at)}</code>\n"
                    f"<b>Швидкість реакції:</b> <code>{get_short_datetime(taken_at - created_at)}</code>")
    else:
        taken_at = "\n"

    messages_text = "\n".join(
        f"\n<code>{get_datetime(el[5])}</code>\n<b>{el[3]}:</b> {el[4]}"
        for el in data_messages
    ) if data_messages else "Немає повідомлень."

    await query.message.edit_text(
        text=f"<code>{get_datetime(created_at)}</code>\n"
             f"<b>Student:</b> {request_text}\n"
             f"{messages_text}\n"
             f"{taken_at}\n"
             f"<b>Status:</b> {status}\n"
             f"{msg}",
        reply_markup=curator_manage_request_keyboard(request_id, query.from_user.id),
        parse_mode="HTML"
    )
