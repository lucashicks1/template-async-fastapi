from abc import abstractmethod
from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):

    @abstractmethod
    def normalise(self) -> dict:
        raise NotImplementedError()


class UUIDMixin:
    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
