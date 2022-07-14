from contextlib import suppress

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


async def is_allowed(session: AsyncSession, user_id: int):
    """
    Checking if user in database

    :param session: сессия БД SQLAlchemy
    :param user_id: Телеграм ID юзера
    """

    user = await session.execute(
        select(User).where(User.tg_id == user_id)
    )
    return user.scalars().all()


async def add_user(session: AsyncSession, user_id: int, user_name: str):
    try:
        user = User()
        user.tg_id = user_id
        user.username = user_name
        session.add(user)
        await session.commit()
        return True
    except IntegrityError:
        return False


async def show_approved_users(session: AsyncSession):
    users = await session.execute(
        select(User)
    )
    return users.scalars(select(User)).all()


async def del_user(session: AsyncSession, user_id: int):
    user = await session.execute(
        delete(User).where(User.tg_id == user_id)
    )
    if user.rowcount == 0:
        return False
    else:
        await session.commit()
        return True
