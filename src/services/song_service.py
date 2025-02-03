from abc import ABC, abstractmethod

from fastapi import HTTPException

from src.models import Song, SongCreate
from src.repositories.song_repository import ISongRepository


class ISongService(ABC):
    @abstractmethod
    async def list_songs(self) -> list[Song]:
        pass

    @abstractmethod
    async def create_song(self, song_data: SongCreate) -> Song:
        pass


class SongService(ISongService):
    def __init__(self, repository: ISongRepository):
        self.repository = repository

    async def list_songs(self) -> list[Song]:
        return await self.repository.get_songs()

    async def create_song(self, song_data: SongCreate) -> Song:
        if await self.repository.get_song_by_name(name=song_data.name):
            raise HTTPException(
                status_code=400,
                detail=f"Song with name: {song_data.name} already exists",
            )

        return await self.repository.add_song(song_data)
