from uuid import UUID

from fastapi import Depends

from template_async_fastapi.database import DB
from template_async_fastapi.repositories import BaseRepository
from template_async_fastapi.models import SongModel
from template_async_fastapi.schemas.song_schema import SongCreate, SongUpdate, SongInDB


class SongRepository(BaseRepository[SongModel, SongInDB]):

    def __init__(self, db: DB = Depends()) -> None:
        super().__init__(SongModel, db)

    async def create(self, data: SongCreate) -> SongInDB:
        return await super().create(data.model_dump())

    async def update(self, uuid: UUID, data: SongUpdate) -> SongInDB:
        return await super().update(uuid, data.model_dump())
