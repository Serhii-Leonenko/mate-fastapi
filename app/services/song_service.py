from fastapi import HTTPException

from app.models import Song, SongCreate
from app.repositories.song_repository import SongRepository


class SongService:
    def __init__(self, repository: SongRepository):
        self.repository = repository

    async def list_songs(self) -> list[Song]:
        return await self.repository.get_songs()

    async def create_song(self, song_data: SongCreate) -> Song:
        if await self.repository.get_song_by_name(name=song_data.name):
            raise HTTPException(status_code=400, detail=f"Song with name: {song_data.name} already exists")

        return await self.repository.add_song(song_data)
