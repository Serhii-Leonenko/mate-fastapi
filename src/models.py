from typing import Optional

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class SongBase(SQLModel):
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    @field_validator("year")
    @classmethod
    def validate_year(cls, value):
        min_year = 1900
        max_year = 2025

        if value is not None and (value < min_year or max_year > 2025):
            raise ValueError("Year must be between 1900 and 202")

        return value
