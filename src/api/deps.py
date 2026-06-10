# src/api/deps.py
from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from core.storage import Storage
from services.player_service import PlayerService
from services.team_service import TeamService


@lru_cache(maxsize=1)
def get_storage() -> Storage:
    return Storage()


StorageDep = Annotated[Storage, Depends(get_storage)]


def get_team_service(storage: StorageDep) -> TeamService:
    return TeamService(storage)


def get_player_service(storage: StorageDep) -> PlayerService:
    return PlayerService(storage)


TeamServiceDep = Annotated[TeamService, Depends(get_team_service)]
PlayerServiceDep = Annotated[PlayerService, Depends(get_player_service)]
