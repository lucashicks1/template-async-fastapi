from uuid import UUID

from fastapi import Depends

from template_async_fastapi.database import DB
from template_async_fastapi.repositories import BaseRepository
from template_async_fastapi.models import ArtistModel
from template_async_fastapi.schemas.artist_schema import ArtistInDB, ArtistCreate, ArtistUpdate


class ArtistRepository(BaseRepository[ArtistModel, ArtistInDB]):
    def __init__(self, db: DB = Depends()) -> None:
        super().__init__(ArtistModel, db)

    async def create(self, data: ArtistCreate) -> ArtistInDB:
        return await super().create(data)

    async def update(self, uuid: UUID, data: ArtistUpdate) -> ArtistInDB:
        return await super().update(uuid, data)
