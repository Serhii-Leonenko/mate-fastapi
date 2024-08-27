from fastapi import APIRouter, Depends

from app.dependencies.services import get_song_service
from app.models import Song, SongCreate
from app.services.song_service import SongService

router = APIRouter()


@router.get("/songs", response_model=list[Song])
async def get_songs(service: SongService = Depends(get_song_service)):
    return await service.list_songs()


@router.post("/songs")
async def add_song(song: SongCreate, service: SongService = Depends(get_song_service)):
    return await service.create_song(song)
