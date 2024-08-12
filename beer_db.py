from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class BeerDataBase(DeclarativeBase):
    pass


class BeerModel(BeerDataBase):
    __tablename__ = "beer_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str] = mapped_column(String(30))
    alcoholic_content: Mapped[float] = mapped_column()
    detail: Mapped[str] = mapped_column(String(255))
    country_origin: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"ID(id={self.id!r}, brand={self.brand!r}, alcoholic content={self.alcoholic_content!r}, detail={self.detail!r}, country_origin={self.country_origin!r})"

