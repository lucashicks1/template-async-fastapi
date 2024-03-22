from template_async_fastapi.models.base_model import BaseModel, UUIDMixin
from sqlalchemy.orm import Mapped,relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from template_async_fastapi.models.song_model import SongModel


class ArtistModel(BaseModel, UUIDMixin):
    __tablename__ = "artists"

    name: Mapped[str]
    songs: Mapped[list["SongModel"]] = relationship(back_populates="artist", lazy="dynamic")

    def normalise(self) -> dict:
        return {
            "name": self.name,
            "songs": self.songs
        }
