from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    created_at: Mapped[DateTime] = Column(DateTime, default=func.now())
    updated_at: Mapped[DateTime] = Column(
        DateTime, default=func.now(), onupdate=func.now()
    )
