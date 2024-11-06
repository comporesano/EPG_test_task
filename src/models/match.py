from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)

from .user import User
from .base import BaseModel


class Match(BaseModel):
    """User matches"""
    
    __tablename__ = "match"
    id = Column(type_=Integer, primary_key=True, autoincrement=True)
    matcher_id = Column(Integer, ForeignKey(User.id))
    target_id = Column(Integer, ForeignKey(User.id))
    