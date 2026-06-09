from enum import Enum
from pydantic import BaseModel


class Position(str, Enum):
    GOALKEEPER = "goalkeeper"
    DEFENDER = "defender"
    MIDFIELDER = "midfielder"
    FORWARD = "forward"


class Team(BaseModel):
    id: int
    name: str
    city: str
    titles: int


class Player(BaseModel):
    id: int
    name: str
    age: int
    position: Position
    team_id: int | None = None
