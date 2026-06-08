from fastapi import APIRouter, status, HTTPException
from api.schemas import TeamCreate, TeamRead
from api.deps import TeamServiceDep
from core.storage import DuplicateTeamNameError, TeamNotEmptyError, UnknownTeamError

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TeamRead)
async def create_team(payload: TeamCreate, service: TeamServiceDep):
    return service.create_team(name=payload.name, city=payload.city, titles=payload.titles)


@router.get("", response_model=list[TeamRead])
async def get_teams(service: TeamServiceDep):
    return service.get_teams()


@router.get("/{team_id}", response_model=TeamRead)
async def get_team(team_id: int, service: TeamServiceDep):
    team = service.get_team(team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: int, service: TeamServiceDep):
    try:
        service.delete_team(team_id)
    except UnknownTeamError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    except TeamNotEmptyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Team has players assigned",
        )
