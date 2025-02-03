from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db import get_session
from src.repositories.song_repository import ISongRepository, SongRepository


def get_song_repository(
    session: AsyncSession = Depends(get_session),
) -> ISongRepository:
    return SongRepository(session)
