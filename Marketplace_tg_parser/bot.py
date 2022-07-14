import asyncio
from aiogram import Bot, Dispatcher, F
import logging

from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import config
from db.base import metadata
from handlers import wb_handler, admin_handler
from middlewares.db import DbSessionMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from middlewares.is_approved import IsApprovedMiddleware

API_TOKEN = '5542713606:AAG1sfpY3tA9Q8teSpOB10YzZuxHOr7feB4'
# https://api.telegram.org/bot5542713606:AAG1sfpY3tA9Q8teSpOB10YzZuxHOr7feB4/getMe
# scheduler = AsyncIOScheduler()
#
#
# async def test(bot: Bot):
#     await bot.send_message(chat_id=630887185, text="test1234")


# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)

    # Создаем engine для PostgreSQL
    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_name}",
        future=True
    )

    # Создаем пул подключений БД
    db_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Создаем бота и диспетчера
    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    # Добавляем фильтр на взаимодействие только в приватных чатах (не группы или каналы)
    dp.message.filter(F.chat.type == "private")

    # Регистрируем мидлварь на подмешивание сессий из пула сессий
    dp.message.middleware(DbSessionMiddleware(db_pool))
    # Мидлварь на проверку наличия пользователя в БД и ограничения доступа к боту если нет в БД
    dp.message.middleware(IsApprovedMiddleware())

    dp.include_router(wb_handler.router)
    dp.include_router(admin_handler.router)




    # scheduler.add_job(test, "interval", seconds=5, args=(bot,))
    # scheduler.start()

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


