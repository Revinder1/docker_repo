from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Update
from db.db_requests import is_allowed

# approved_list = [630887185, ]


class IsApprovedMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]):
        # Верификация юзера есть ли он в БД, ограничение доступа к дальнейшим действиям если нет
        user = await is_allowed(data["session"], event.chat.id)
        if not user:
            await event.answer(f"Вас нет в списке допущенных к боту!\n"
                               f"Ваш Telegram ID: {event.chat.id}\nВаш Username: {event.chat.username}\n"
                               f"Обратитесь к @Revinder2 c этими данными для получения доступа")
            print(event.chat.id, event.chat.username)
            return
        return await handler(event, data)
