from typing import Optional

from sqlmodel import Field, SQLModel


class SongBase(SQLModel):

    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass
