from fastapi import Depends

from src.dependencies.repositories import get_song_repository
from src.repositories.song_repository import ISongRepository
from src.services.song_service import ISongService, SongService


def get_song_service(
    song_repository: ISongRepository = Depends(get_song_repository),
) -> ISongService:
    return SongService(song_repository)
