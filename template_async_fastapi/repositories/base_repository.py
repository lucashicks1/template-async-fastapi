from uuid import UUID
from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from template_async_fastapi.models.base_model import BaseModel
from template_async_fastapi.database import DB
from fastapi import Depends
from pydantic import BaseModel as SchemaBaseModel

Model = TypeVar("Model", bound=BaseModel)


class BaseRepository(ABC, Generic[Model]):
    db: DB
    model: Model

    def __init__(self, model: type(Model), db: DB = Depends()) -> None:
        self.db = db
        self.model = model

    @abstractmethod
    async def get(self, uuid: UUID) -> SchemaBaseModel | None:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            return None
        return SchemaBaseModel(**result.normalise())

    @abstractmethod
    async def create(self, data: dict) -> SchemaBaseModel:
        model_instance: Model = self.model(**data)
        self.db.add(model_instance)
        await self.db.commit()
        await self.db.refresh(model_instance)
        return SchemaBaseModel(**model_instance.normalise())

    @abstractmethod
    async def update(self, uuid: UUID, data: dict) -> SchemaBaseModel | None:
        result: Model | None = await self.db.get(self.model, uuid)
        if not result:
            return None
        for key, value in data.items():
            setattr(result, key, value)
        await self.db.commit()
        await self.db.refresh(result)
        return SchemaBaseModel(**result.normalise())
