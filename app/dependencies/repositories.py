from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.repositories.song_repository import SongRepository


def get_song_repository(session: AsyncSession = Depends(get_session)) -> SongRepository:
    return SongRepository(session)
