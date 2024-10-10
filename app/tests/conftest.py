import json

import asyncio
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import pytest
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

from app.config import settings
from app.database import engine, Base, async_session_maker

from app.cities.models import City

from httpx import AsyncClient, ASGITransport
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    redis_client = await aioredis.from_url("redis://localhost:6379", decode_responses=False)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    cities = open_mock_json("cities")

    async with async_session_maker() as session:
        add_cities = insert(City).values(cities)

        await session.execute(add_cities)
        await session.commit()

@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac