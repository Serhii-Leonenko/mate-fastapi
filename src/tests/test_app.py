import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_songs_empty(async_client: AsyncClient):
    response = await async_client.get("/songs")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_song(async_client: AsyncClient):
    song_data = {
        "name": "Test Song",
        "artist": "Test Artist",
        "year": 2000,
    }
    response = await async_client.post("/songs", json=song_data)
    assert response.status_code == 200, response.text
    created_song = response.json()
    assert created_song["id"] is not None
    assert created_song["name"] == song_data["name"]
    assert created_song["artist"] == song_data["artist"]
    assert created_song["year"] == song_data["year"]

    response = await async_client.get("/songs")
    assert response.status_code == 200
    songs = response.json()
    assert isinstance(songs, list)
    assert any(song["name"] == song_data["name"] for song in songs)


@pytest.mark.asyncio
async def test_create_duplicate_song(async_client: AsyncClient):
    song_data = {
        "name": "Duplicate Song",
        "artist": "Artist",
        "year": 1999,
    }
    response = await async_client.post("/songs", json=song_data)
    assert response.status_code == 200, response.text

    response = await async_client.post("/songs", json=song_data)
    assert response.status_code == 400
    error_detail = response.json().get("detail")
    assert error_detail is not None
    assert "already exists" in error_detail
