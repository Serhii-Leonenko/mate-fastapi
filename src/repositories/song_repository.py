from abc import ABC

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Song, SongCreate


class ISongRepository(ABC):
    async def get_song_by_name(self, name: str) -> Song | None:
        pass

    async def get_songs(self) -> list[Song]:
        pass

    async def add_song(self, song_data: SongCreate) -> Song:
        pass


class SongRepository(ISongRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_song_by_name(self, name: str) -> Song | None:
        return await self.session.scalar(select(Song).where(Song.name == name))

    async def get_songs(self) -> list[Song]:
        result = await self.session.scalars(select(Song))

        return result.all()

    async def add_song(self, song_data: SongCreate) -> Song:
        song = Song(name=song_data.name, artist=song_data.artist, year=song_data.year)
        self.session.add(song)
        await self.session.commit()
        await self.session.refresh(song)

        return song
