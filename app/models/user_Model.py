from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.db import Base

class user_Model(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(191), nullable=False, unique=True, index=True)
    email = Column(String(191), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
