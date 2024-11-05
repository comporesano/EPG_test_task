from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache

import os


class Config(BaseSettings):
    
    DB_USER: str
    DB_PASS: str
    DB_HOST: str 
    DB_PORT: str 
    DB_NAME: str
        
    model_config = SettingsConfigDict(env_file=load_dotenv(), extra="ignore")
    

@lru_cache
def get_config() -> Config:
    return Config()