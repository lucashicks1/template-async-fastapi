from pydantic import BaseModel
from datetime import date
from uuid import UUID


class SongUpdate(BaseModel):
    name: str | None = None
    duration: int | None = None
    release_date: date | None = None
    artist_uuid: UUID | None = None


class SongCreate(SongUpdate):
    name: str
    duration: int
    release_date: date
    artist_uuid: UUID


class SongInDB(SongCreate):
    uuid: UUID
