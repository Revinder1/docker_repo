import asyncio
from aiogram import Bot, Dispatcher
import logging

from apscheduler.triggers.cron import CronTrigger

from handlers import wb_handler
from middlewares.is_approved import IsApprovedMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler



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
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(wb_handler.router)
    # СДЕЛАТЬ КОННЕКТ ЧЕРЕЗ МИДЛВАРЬ К ДБ И ПРОВЕРЯТЬ ЕСТЬ ЛИ ПОЛЬЗОВАТЕЛЬ В СПИСКЕ ДОПУЩЕННЫХ
    dp.message.outer_middleware(IsApprovedMiddleware())
    #
    # scheduler.add_job(test, "interval", seconds=5, args=(bot,))
    # scheduler.start()
    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


