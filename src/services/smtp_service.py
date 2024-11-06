from settings import get_settings

from email.message import EmailMessage

from functools import lru_cache

import smtplib


class SmtpService:
    """SMTP service for sending mail"""
    def __init__(self) -> None:
        self.__driver = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
        self.__driver.login(user=get_settings().MAIL_LOGIN, 
                            password=get_settings().MAIL_PASSW)
        
    def send_message(self, 
                     source_mail: str, 
                     target_mail: str, 
                     msg_title: str,
                     message: str) -> True:
        try:
            msg = EmailMessage()
            msg.set_content(message)
            msg["Subject"] = msg_title
            msg["From"] = source_mail
            msg["To"] = target_mail
            with self.__driver as smtp:
                smtp.send_message(msg=msg)
        except Exception:
            return False
        else:
            return True


@lru_cache
def smtp_service() -> SmtpService:
    return SmtpService()
