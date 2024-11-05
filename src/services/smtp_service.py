from settings import get_settings

from functools import lru_cache

import smtplib


class SmtpService:
    """SMTP service for sending mail"""
    def __init__(self) -> None:
        self.__driver = smtplib.SMTP("smtp.gmail.com", 587)
        self.__driver.starttls()
        self.__driver.login(user=get_settings().GMAIL_LOGIN, 
                            password=get_settings().GMAIL_PASSW)
        
    def send_message(self, 
                     source_mail: str, 
                     target_mail: str, 
                     message: str) -> True:
        try:
            self.__driver.send_message(
                msg=message,
                from_addr=source_mail,
                to_addrs=target_mail
            )
        except Exception:
            return False
        else:
            return True


@lru_cache
def smtp_service() -> SmtpService:
    return SmtpService()
    