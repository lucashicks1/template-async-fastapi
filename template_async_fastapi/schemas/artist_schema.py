from uuid import UUID
from pydantic import BaseModel


class ArtistUpdate(BaseModel):
    name: str | None = None


class ArtistCreate(ArtistUpdate):
    name: str


class ArtistInDB(ArtistCreate):
    uuid: UUID
