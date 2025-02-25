from aiogram.fsm.state import StatesGroup, State


class RequestSupport(StatesGroup):
    request_id = State()
    waiting_for_request = State()
    processing_request = State()


class Support(StatesGroup):
    request_id = State()
    processing_request = State()
