from sqlalchemy import insert, select

from functools import lru_cache

from datetime import datetime

from services import smtp_service, user_operating_service
from settings import get_settings
from models import Match
from db import asm


class MatchOperatingService:
    """CDU match service"""
    def __init__(self) -> None:
        self._session = asm()
        self.__model = Match
    
    async def add_one(self, data: dict) -> int:
            matcher_id = data.get("matcher_id")
            target_id = data.get("target_id")
            
            smtps = smtp_service()
            uos = user_operating_service()
            matcher_user = await uos.get(id=matcher_id)
            matcher_user = matcher_user.scalar_one_or_none()
            target_user = await uos.get(id=target_id)
            target_user = target_user.scalar_one_or_none()
            match = await self.get(matcher_id=target_id)
            matches = match.scalars().all()    
            await self.check_updates_matches(user=matcher_user, user_service=uos)
            user_matches = await self.check_matches(user=matcher_user)
            if user_matches  > 0:
                query = insert(self.__model).values(**data).returning(self.__model.id)
                await self._session.execute(query)
                await self._session.commit()
                await uos.update_one(id=matcher_id, data={"matches": matcher_user.matches - 1})
                for match in matches:
                    if matcher_id == match.target_id:
                        smtps.send_message(
                            source_mail=get_settings().MAIL_LOGIN,
                            target_mail=target_user.e_mail,
                            msg_title="У Вас взаимная симпатия!",
                            message=f"Вы понравились {matcher_user.first_name}! Почта участника: {matcher_user.e_mail}"
                        )
                        smtps.send_message(
                            source_mail=get_settings().MAIL_LOGIN,
                            target_mail=matcher_user.e_mail,
                            msg_title="У Вас взаимная симпатия!",
                            message=f"Вы понравились {matcher_user.first_name}! Почта участника: {matcher_user.e_mail}"
                        )
                        break
                smtps.close()
            else:
                raise
    
    async def get(self, matcher_id: int):
        query = select(self.__model).where(getattr(self.__model, "matcher_id") == matcher_id)
        result = await self._session.execute(query)
        return result
    
    async def check_matches(self, user) -> bool:
        if user.matches > 0:
            return True
        else:
            return False
    
    async def check_updates_matches(self, user, user_service) -> bool:
        try:
            match_update_date = datetime.fromisoformat(str(user.matches_update))       
            current_date = datetime.now()
            
            differrence = current_date - match_update_date
            
            if differrence.days > 0:
                await user_service.update_one(id=user.id, data={"matches": 5, "matches_update": current_date}) 
        except TypeError:
            raise
    

@lru_cache
def match_service() -> MatchOperatingService:
    return MatchOperatingService()
