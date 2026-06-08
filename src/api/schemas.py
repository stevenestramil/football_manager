from pydantic import BaseModel, Field, field_validator
from core.models import Position


def _strip(v: str) -> str:
    return v.strip() if isinstance(v, str) else v


class TeamCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    city: str = Field(min_length=2, max_length=50)
    titles: int = Field(ge=0)

    _strip_name = field_validator("name", "city", mode="before")(_strip)


class TeamRead(BaseModel):
    id: int
    name: str
    city: str
    titles: int


class PlayerCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=16, le=45)
    position: Position
    team_id: int | None = None

    _strip_name = field_validator("name", "city", mode="before")(_strip)

class PlayerTeamAssign(BaseModel):
    team_id: int
