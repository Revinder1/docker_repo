from contextlib import suppress

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def is_allowed(session: AsyncSession, user_id: int):
    """
    Checking if user in database

    :param session: SQLAlchemy DB session
    :param user_id: user's Telegram ID
    """

    user = await session.execute(
        select(User).where(User.tg_id == user_id)
    )
    return user.scalars().all()


async def add_user(session: AsyncSession, user_id: int, user_name: str):
    user = User()
    user.tg_id = user_id
    user.username = user_name
    session.add(user)
    with suppress(IntegrityError):
        await session.commit()
