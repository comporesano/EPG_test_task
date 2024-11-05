from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from models import Match
from db import asm


class MatchOperatingService:
    """CDU match service"""
    def __init__(self) -> None:
        self._session = asm()
        self.__model = Match
    
    async def add_one(self, data: dict) -> int:
        query = insert(self.__model).values(**data).returning(self.__model.id)
        result = await self._session.execute(query)
        await self._session.commit()
        
        return result
    