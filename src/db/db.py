from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import get_settings


ENGINE_ARGS = dict(pool_size=50, pool_pre_ping=True, pool_recycle=3600)
db_params = {
    "drivername": "postgresql+asyncpg",
    "host": get_settings().DB_HOST,
    "port": get_settings().DB_PORT,
    "database": get_settings().DB_NAME,
    "username": get_settings().DB_USER,
    "password": get_settings().DB_PASS,    
}

def get_session_maker(conn_params: dict[str, str]) -> async_sessionmaker[AsyncSession]:
    async_url = URL.create(**conn_params)
    async_engine = create_async_engine(async_url, **ENGINE_ARGS)
    
    return async_sessionmaker(async_engine, expire_on_commit=False, autoflush=True)

asm = get_session_maker(db_params)
