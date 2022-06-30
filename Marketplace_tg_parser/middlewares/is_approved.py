from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update

approved_list = [630887185, ]


class IsApprovedMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]):
        if event.from_user.id not in approved_list:
            await event.answer("Вас нет в списке допущенных к боту! Обратитесь к @Revinder2 для получения доступа")
            print(event.from_user.id, event.from_user.first_name)
            return
        return await handler(event, data)
