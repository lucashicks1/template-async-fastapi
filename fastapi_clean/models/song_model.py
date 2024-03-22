from uuid import UUID
from fastapi_clean.models.base_model import BaseModel
from fastapi_clean.models.base_model import UUIDMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from fastapi_clean.models.artist_model import ArtistModel


class SongModel(BaseModel, UUIDMixin):
    __tablename__ = "songs"

    name: Mapped[str]
    duration: Mapped[int]
    artist_uuid: Mapped[UUID] = mapped_column(ForeignKey(ArtistModel.uuid))

    artist: Mapped[ArtistModel] = relationship(back_populates="songs", lazy="dynamic")

    def normalise(self) -> dict:
        return {
            "name": self.name,
            "duration": self.duration,
            "artist_uuid": self.artist_uuid,
            "artist": self.artist
        }


