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
    GMAIL_LOGIN: str
    GMAIL_PASSW: str
        
    model_config = SettingsConfigDict(env_file=os.path.join(GLOBAL_PATH, "src", ".env"), 
                                      extra="ignore")
    

@lru_cache
def get_settings() -> Settings:
    return Settings()
