from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Update
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_requests import is_allowed, add_user


# approved_list = [630887185, ]


class IsApprovedMiddleware(BaseMiddleware):
    # def __init__(self, session: AsyncSession):
    #     self.session = session

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]):
        # ПРОБУЮ СДЕЛАТЬ ВЕРИФИКАЦИЮ ПОЛЬЗОВАТЕЛЯ ЗДЕСЬ
        user = await is_allowed(data["session"], event.chat.id)
        if not user:
            await event.answer("Вас нет в списке допущенных к боту! Обратитесь к @Revinder2 для получения доступа")
            print(event.chat.id, event.chat.username)
            # await add_user(data["session"], event.chat.id, event.chat.username)
            return
        return await handler(event, data)
