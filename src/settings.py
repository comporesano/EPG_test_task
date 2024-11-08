from utils import GLOBAL_PATH

from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache

import os


class Settings(BaseSettings):
    
    DB_USER: str
    DB_PASS: str
    DB_HOST: str 
    DB_PORT: str 
    DB_NAME: str
    MAIL_LOGIN: str
    MAIL_PASSW: str
        
    model_config = SettingsConfigDict(env_file=os.path.join(GLOBAL_PATH, ".env"), 
                                      extra="ignore")
    

@lru_cache
def get_settings() -> Settings:
    return Settings()
