from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import Song, SongCreate


class SongRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_song_by_name(self, name: str) -> Song | None:
        result = await self.session.execute(select(Song).where(Song.name == name))
        song = result.scalar_one_or_none()

        return song

    async def get_songs(self) -> list[Song]:
        result = await self.session.execute(select(Song))
        songs = result.scalars().all()

        return songs

    async def add_song(self, song_data: SongCreate) -> Song:
        song = Song(name=song_data.name, artist=song_data.artist, year=song_data.year)
        self.session.add(song)
        await self.session.commit()
        await self.session.refresh(song)

        return song
