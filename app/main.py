from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.cities.router import router as cities_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.service.cache import clear_cache


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost", decode_responses=False)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Поиск ближайшего города",
    version="0.1.0",
    root_path="/api",
    lifespan=lifespan
)

app.include_router(cities_router)


@app.get("/health")
async def ping():
    await clear_cache()
    return {"status": "OK", "message": "pong"}


@app.get("/clear-cache")
async def ping():
    try:
        await clear_cache()
        return {"status": "OK", "message": "cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
