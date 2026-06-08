# src/api/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from core.db import get_session
from core.storage import Storage
from services.player_service import PlayerService
from services.team_service import TeamService


SessionDep = Annotated[Session, Depends(get_session)]


def get_storage(session: SessionDep) -> Storage:
    return Storage(session)


StorageDep = Annotated[Storage, Depends(get_storage)]


def get_team_service(storage: StorageDep) -> TeamService:
    return TeamService(storage)


def get_player_service(storage: StorageDep) -> PlayerService:
    return PlayerService(storage)


TeamServiceDep = Annotated[TeamService, Depends(get_team_service)]
PlayerServiceDep = Annotated[PlayerService, Depends(get_player_service)]