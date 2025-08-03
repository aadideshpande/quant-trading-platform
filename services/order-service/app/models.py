from sqlalchemy import Column, Integer, String, DateTime, func
from .db import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    quantity = Column(Integer)
    side = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

