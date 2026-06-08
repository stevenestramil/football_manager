from fastapi import APIRouter, HTTPException, status
from api.schemas import PlayerCreate, PlayerTeamAssign
from api.deps import PlayerServiceDep
from core.models import Position
from core.storage import UnknownPlayerError, UnknownTeamError

router = APIRouter(prefix="/players", tags=["players"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_player(player: PlayerCreate, service: PlayerServiceDep):
    try:
        created = service.create_player(
            name=player.name, age=player.age, position=player.position, team_id=player.team_id
        )
    except UnknownTeamError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return created


@router.get("")
async def get_players(
    service: PlayerServiceDep,
    team_id: int | None = None,
    position: Position | None = None,
    min_age: int | None = None,
):
    return service.get_players(team_id=team_id, position=position, min_age=min_age)


@router.get("/{player_id}")
async def get_player(player_id: int, service: PlayerServiceDep):
    player = service.get_player(player_id=player_id)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    return player


@router.patch("/{player_id}/team")
async def add_player_to_team(
    player_id: int, team_assign: PlayerTeamAssign, service: PlayerServiceDep
):
    try:
        return service.assign_player_to_team(player_id=player_id, team_id=team_assign.team_id)
    except UnknownPlayerError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    except UnknownTeamError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")


@router.delete("/{player_id}/team", status_code=status.HTTP_204_NO_CONTENT)
async def remove_player_from_team(player_id: int, service: PlayerServiceDep):
    try:
        service.remove_player_from_team(player_id)
    except UnknownPlayerError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, service: PlayerServiceDep):
    try:
        service.delete_player(player_id)
    except UnknownPlayerError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
