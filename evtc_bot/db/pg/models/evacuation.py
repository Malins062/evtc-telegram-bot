from evtc_bot.db.pg.models.base import Base


class Evacuation(Base):
    __tablename__ = "evacuations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    evacuated_at: Mapped[DateTime] = mapped_column(DateTime)
    car_model: Mapped[str] = mapped_column(String(25), nullable=False)
    car_number: Mapped[str] = mapped_column(String(9), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    article: Mapped[str] = mapped_column(String(300), nullable=False)
    parking: Mapped[str] = mapped_column(String(100), nullable=False)
    protocol: Mapped[str] = mapped_column(String(10), nullable=False)
