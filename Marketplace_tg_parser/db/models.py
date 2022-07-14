from sqlalchemy import String, Column, BigInteger
from db.base import Base


class User(Base):
    """Implements base table contains all registered in bot users"""

    __tablename__ = "users"

    tg_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String, default=None)


    def __repr__(self) -> str:
        return f"User: {self.tg_id}, {self.username}"

    def __str__(self) -> str:
        return f"User: {self.tg_id}, {self.username}"

