from uuid import UUID
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from template_async_fastapi.repositories import BaseRepository
from pydantic import BaseModel
from fastapi import Depends

Repository = TypeVar("Repository", bound=BaseRepository)


class BaseService(ABC, Generic[Repository]):
    repository: Repository

    @abstractmethod
    def __init__(self, repository: Repository = Depends()):
        raise NotImplementedError()

    @abstractmethod
    async def get(self, uuid: UUID) -> BaseModel:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, data: BaseModel) -> BaseModel:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, uuid: UUID, data: BaseModel) -> BaseModel:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, uuid: UUID) -> None:
        raise NotImplementedError()
