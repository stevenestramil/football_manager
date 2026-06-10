from pydantic import BaseModel, ConfigDict, Field, field_validator
from core.enums import Position


def _strip(v: str) -> str:
    return v.strip() if isinstance(v, str) else v


class PlayerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    age: int
    position: Position
    team_id: int | None = None


class TeamCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    city: str = Field(min_length=2, max_length=50)
    titles: int = Field(ge=0)

    _strip_name = field_validator("name", "city", mode="before")(_strip)


class TeamSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    city: str
    titles: int


class TeamRead(TeamSummary):
    players: list[PlayerRead] = []


class PlayerCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=16, le=45)
    position: Position
    team_id: int | None = None

    _strip_name = field_validator("name", mode="before")(_strip)


class PlayerTeamAssign(BaseModel):
    team_id: int
