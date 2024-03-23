from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from template_async_fastapi.services import BaseService
from template_async_fastapi.repositories import ArtistRepository
from template_async_fastapi.schemas.artist_schema import ArtistCreate, ArtistUpdate, ArtistInDB
from template_async_fastapi.exceptions import NotFoundException
from loguru import logger


class ArtistService(BaseService):
    def __init__(self, repository: ArtistRepository = Depends()):
        self.repository = repository

    async def get(self, uuid: UUID) -> ArtistInDB:
        try:
            result = await self.repository.get(uuid)
        except NotFoundException as e:
            logger.error(e)
            raise
        return result

    async def create(self, data: ArtistCreate) -> ArtistInDB:
        return await self.repository.create(data)

    async def update(self, uuid: UUID, data: ArtistUpdate) -> ArtistInDB:
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
