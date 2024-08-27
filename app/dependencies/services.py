from fastapi import Depends

from app.dependencies.repositories import get_song_repository
from app.services.song_service import SongService


def get_song_service(song_repository=Depends(get_song_repository)) -> SongService:
    return SongService(song_repository)
