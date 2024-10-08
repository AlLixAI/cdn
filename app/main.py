from fastapi import FastAPI
from app.cities.router import router as cities_router

app = FastAPI(
    title="Поиск ближайшего города",
    version="0.1.0",
    root_path="/api"
)

app.include_router(cities_router)


@app.get("/health")
async def ping():
    return {"status": "OK", "message": "pong"}
