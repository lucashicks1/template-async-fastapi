from uuid import UUID
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from template_async_fastapi.models.base_model import BaseModel
from template_async_fastapi.database import DB
from fastapi import Depends
from pydantic import BaseModel as SchemaBaseModel
from template_async_fastapi.exceptions import NotFoundException

Model = TypeVar("Model", bound=BaseModel)
SchemaModel = TypeVar("SchemaModel", bound=SchemaBaseModel)


class BaseRepository(ABC, Generic[Model, SchemaModel]):
    db: DB
    model: Model

    @abstractmethod
    def __init__(self, model: type(Model), db: DB = Depends()) -> None:
        self.db = db
        self.model = model

    async def get(self, uuid: UUID) -> SchemaModel:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise NotFoundException()
        return SchemaBaseModel(**result.normalise())

    @abstractmethod
    async def create(self, data: dict) -> SchemaModel:
        # noinspection PyCallingNonCallable
        model_instance: Model = self.model(**data)
        self.db.add(model_instance)
        await self.db.commit()
        await self.db.refresh(model_instance)
        return SchemaBaseModel(**model_instance.normalise())

    @abstractmethod
    async def update(self, uuid: UUID, data: dict) -> SchemaModel:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise NotFoundException
        for key, value in data.items():
            setattr(result, key, value)
        await self.db.commit()
        await self.db.refresh(result)
        return SchemaBaseModel(**result.normalise())

    async def delete(self, uuid: UUID) -> None:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            raise NotFoundException
        await self.db.delete(result)
        await self.db.commit()
