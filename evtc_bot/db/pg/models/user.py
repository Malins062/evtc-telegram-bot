from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from evtc_bot.db.pg.models.base import DeclarativeBase
from evtc_bot.db.pg.models.evacuation import Evacuation
from evtc_bot.db.redis.models import Role


class User(DeclarativeBase):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(BigInteger)
    name: Mapped[str] = Column(String(150), nullable=True)
    full_name: Mapped[str] = Column(String(150), nullable=True)
    phone_number: Mapped[str] = Column(String(20), nullable=True)
    role: Mapped[Role] = Column(default=Role.inspector)
    allowed: Mapped[Boolean] = Column(default=True)
    evacuations = relationship(Evacuation, backref="evacuations", default=[])
