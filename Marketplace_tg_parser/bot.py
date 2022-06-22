import asyncio
from aiogram import Bot, Dispatcher
import logging
from handlers import wb_handler



API_TOKEN = '5542713606:AAG1sfpY3tA9Q8teSpOB10YzZuxHOr7feB4'
# https://api.telegram.org/bot5542713606:AAG1sfpY3tA9Q8teSpOB10YzZuxHOr7feB4/getMe


# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(wb_handler.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())


