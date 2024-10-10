from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
