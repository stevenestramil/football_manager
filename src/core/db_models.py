from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.enums import Position


class TeamORM(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    city: Mapped[str] = mapped_column(String(50))
    titles: Mapped[int]

    players: Mapped[list["PlayerORM"]] = relationship(back_populates="team")


class PlayerORM(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]
    position: Mapped[Position]
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)

    team: Mapped[TeamORM | None] = relationship(back_populates="players")
