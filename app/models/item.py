from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, func
from app.db.db import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    category = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
