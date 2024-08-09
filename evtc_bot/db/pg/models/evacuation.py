from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped

from evtc_bot.db.pg.models.base import DeclarativeBase


class Evacuation(DeclarativeBase):
    __tablename__ = "evacuations"

    id: Mapped[int] = Column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = Column(BigInteger, ForeignKey("users.user_id"))
    evacuated_at: Mapped[DateTime] = Column(DateTime, nullable=False)
    car_model: Mapped[str] = Column(String(25), nullable=False)
    car_number: Mapped[str] = Column(String(9), nullable=False)
    address: Mapped[str] = Column(String(100), nullable=False)
    article: Mapped[str] = Column(String(300), nullable=False)
    parking: Mapped[str] = Column(String(100), nullable=False)
    protocol: Mapped[str] = Column(String(10), nullable=False)
