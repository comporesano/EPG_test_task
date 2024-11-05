from sqlalchemy import delete, insert, update, select
from sqlalchemy.exc import IntegrityError

from functools import lru_cache

from models import User
from db import asm


class UserOperatingService:
    """CDU(Create, delete, update) user service"""
    def __init__(self) -> None:
        self._session = asm()
        self.__model = User
        
    async def add_one(self, data: dict) -> int:
        try:
            query = insert(self.__model).values(**data).returning(self.__model.id)
            result = await self._session.execute(query)
            await self._session.commit()
            
            return result
        except IntegrityError:
            raise

    async def add_list(self, list_data: list[dict]) -> dict[str, list[int]]:
        error_list = []
        result_list = []
        for user_data in list_data:
            try:
                result = await self.add_one(data=user_data)
                result_list.append(result)
            except IntegrityError:
                error_list.append(user_data)
        
        return dict(zip(
            ['added', 'not_added'],
            [result_list, error_list],
        ))

    async def delete_one(self, id: int) -> int | None:
        query = delete(self.__model).where(getattr(self.__model, "id") == id).returning(1)
        result = await self._session.execute(query)
        await self._session.commit()
        
        return result

    async def delete_list(self, list_id: list) -> dict[str, list[int]]:
        error_list = []
        result_list = []
        for id in list_id:
            result = await self.delete_one(id=id)
            if result:
                result_list.append(result)
            else:
                error_list.append(result)
    
    async def delete_all(self) -> bool:
        try:
            query = delete(self.__model)
            await self._session.execute(query)
        except Exception:
            raise
    
    async def update_one(self, id: int, data: dict) -> int:
        try:
            query = update(self.__model).values(**data).filter_by(id=id).returning(self.__model.id)
            result = await self._session.execute(query)
            await self._session.commit()
            return result
        except IntegrityError:
            raise
    
    async def update_list(self, list_to_update: dict[int, dict]) -> dict[str, list]:
        error_list = []
        result_list = []
        for id in list_to_update:
            try:
                data = list_to_update[id]
                result = await self.update_one(id=id, data=data)
                result_list.append(result)
            except IntegrityError:
                error_list.append(data)
        
        return dict(zip(
            ['added', 'not_added'],
            [result_list, error_list],
        ))
    
    async def get_one(self, id: int):
        query = select(self.__model).where(getattr(self.__model, "id") == id)
        result = await self._session.execute(query)
        return result
    

@lru_cache
def user_operating_service() -> UserOperatingService:
    return UserOperatingService()
