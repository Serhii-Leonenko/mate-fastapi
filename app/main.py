from fastapi import FastAPI

from app.db import init_db
from app.routes import song_routes

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


app.include_router(song_routes.router)
