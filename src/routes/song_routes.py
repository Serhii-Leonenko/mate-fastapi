from fastapi import APIRouter, Depends

from src.dependencies.services import get_song_service
from src.models import Song, SongCreate
from src.services.song_service import ISongService, SongService

router = APIRouter()


@router.get("/songs", response_model=list[Song])
async def get_songs(service: ISongService = Depends(get_song_service)):
    return await service.list_songs()


@router.post("/songs")
async def add_song(song: SongCreate, service: ISongService = Depends(get_song_service)):
    return await service.create_song(song)
