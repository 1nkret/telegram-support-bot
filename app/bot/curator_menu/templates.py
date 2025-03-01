from app.bot.curator_menu.keyboards import curator_manage_request_keyboard
from app.utils.find_args import find_args
from app.utils.get_datetime import get_datetime, get_short_datetime
from database.crud import get_request, get_messages


async def get_manage_menu(request_id, from_user_id, msg: str = ""):
    data = get_request(request_id)

    request_text = data[2]
    created_at = data[3]
    status = data[4]
    taken_at = data[6]

    if taken_at:
        taken_at = (f"<b>Request taken at:</b> <code>{get_datetime(taken_at)}</code>\n"
                    f"<b>Reaction speed:</b> <code>{get_short_datetime(taken_at - created_at)}</code>")
    else:
        taken_at = "\n"

    text = (f"<code>{get_datetime(created_at)}</code>\n"
             f"<b>Student:</b> {request_text}\n"
             f"{taken_at}\n"
             f"<b>Status:</b> {status}\n"
             f"{msg}")
    kb = curator_manage_request_keyboard(request_id, from_user_id)

    return text, kb
