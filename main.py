import asyncio
from aiogram import Bot, Dispatcher

from core.config import BOT_TOKEN
from database.db import create_database, create_tables
from app.utils.load_routers import load_routers


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    create_database()
    create_tables()
    dp.include_router(load_routers())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())