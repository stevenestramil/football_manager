from fastapi import APIRouter, status, HTTPException
from api.schemas import PlayerRead, TeamCreate, TeamRead, TeamSummary
from api.deps import PlayerServiceDep, TeamServiceDep
from core.storage import DuplicateTeamNameError, TeamNotEmptyError, UnknownTeamError

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TeamRead)
async def create_team(payload: TeamCreate, service: TeamServiceDep):
    try:
        return service.create_team(name=payload.name, city=payload.city, titles=payload.titles)
    except DuplicateTeamNameError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A team with that name already exists",
        )


@router.get("", response_model=list[TeamSummary])
async def get_teams(team_service: TeamServiceDep):
    return team_service.get_teams()


@router.get("/{team_id}", response_model=TeamRead)
async def get_team(
    team_id: int, team_service: TeamServiceDep, player_service: PlayerServiceDep
):
    team = team_service.get_team(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return TeamRead(
        **team.model_dump(),
        players=[PlayerRead.model_validate(p) for p in player_service.get_players(team_id=team_id)],
    )


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, team_service: TeamServiceDep):
    try:
        team_service.delete_team(team_id)
    except UnknownTeamError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    except TeamNotEmptyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team has players assigned",
        )
