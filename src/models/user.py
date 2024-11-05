from sqlalchemy import Column, Integer, LargeBinary, String

from .base import BaseModel


class User(BaseModel):
    """User table model"""
    
    __tablename__ = "user"
    id = Column(type_=Integer, autoincrement=True, primary_key=True, nullable=False)
    avatar = Column(type_=LargeBinary, nullable=True)
    e_mail = Column(type_=String(length=30), unique=True, nullable=False)
    first_name = Column(type_=String(length=10), nullable=False)
    last_name = Column(type_=String(length=15), nullable=False)
    sex = Column(type_=String(length=6), nullable=False, default="male")
    