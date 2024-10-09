import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.cities.router import router as cities_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.service.cache import clear_cache

from prometheus_fastapi_instrumentator import Instrumentator

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://cdn_redis:6379", decode_responses=False)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Поиск ближайшего города",
    version="0.1.0",
    root_path="/api",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cities_router)
instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=["/metrics"],
)
instrumentator.instrument(app).expose(app)

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