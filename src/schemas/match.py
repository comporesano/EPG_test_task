from typing import Optional
from pydantic import BaseModel, Field


class MatchBase(BaseModel):
    """Match base scheme"""
    pass

    class Config:
        orm_mode = True 


class MatchCreateScheme(MatchBase):
    """Create match scheme"""
    matcher_id: Optional[int] = Field(...)
    target_id: Optional[int] = Field(...)
    