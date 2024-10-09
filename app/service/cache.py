from fastapi_cache import FastAPICache


async def clear_cache():
    await FastAPICache.clear()
