from fastapi import FastAPI

from src.routes import song_routes

app = FastAPI()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


app.include_router(song_routes.router)
