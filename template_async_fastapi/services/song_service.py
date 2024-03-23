from uuid import UUID

from fastapi import Depends

from template_async_fastapi.services import BaseService
from template_async_fastapi.repositories import SongRepository
from template_async_fastapi.schemas.song_schema import SongCreate, SongUpdate, SongInDB
from template_async_fastapi.exceptions import NotFoundException
from loguru import logger


class SongService(BaseService):
    def __init__(self, repository: SongRepository = Depends()):
        self.repository = repository

    async def get(self, uuid: UUID) -> SongInDB:
        try:
            result = await self.repository.get(uuid)
        except NotFoundException as e:
            logger.error(e)
            raise
        return result

    async def create(self, data: SongCreate) -> SongInDB:
        return await self.repository.create(data)

    async def update(self, uuid: UUID, data: SongUpdate) -> SongInDB:
        try:
            result = await self.repository.update(uuid, data)
        except NotFoundException as e:
            logger.error(e)
            raise
        return result

    async def delete(self, uuid: UUID) -> None:
        try:
            await self.repository.delete(uuid)
        except NotFoundException as e:
            logger.error(e)
            raise
        return None
