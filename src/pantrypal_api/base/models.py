from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PantryPalBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
