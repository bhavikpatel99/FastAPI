from sqlalchemy import Column, Integer, String, Text, Numeric, TIMESTAMP, func
from app.db.db import Base

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
