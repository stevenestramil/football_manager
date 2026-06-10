from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db_models import Player, Team
from core.enums import Position


class TeamNotEmptyError(Exception):
    def __init__(self, team_id: int):
        self.team_id = team_id


class DuplicateTeamNameError(Exception):
    def __init__(self, name: str):
        self.name = name


class UnknownTeamError(Exception):
    def __init__(self, team_id: int):
        self.team_id = team_id


class UnknownPlayerError(Exception):
    def __init__(self, player_id: int):
        self.player_id = player_id


class Storage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_team(self, name: str, city: str, titles: int) -> Team:
        existing = await self.session.scalar(
            select(Team).where(func.lower(Team.name) == name.lower())
        )
        if existing is not None:
            raise DuplicateTeamNameError(name)
        team = Team(name=name, city=city, titles=titles)
        self.session.add(team)
        await self.session.commit()
        await self.session.refresh(team)
        return team

    async def get_teams(self) -> list[Team]:
        result = await self.session.scalars(select(Team))
        return list(result)

    async def get_team(self, team_id: int) -> Team | None:
        return await self.session.scalar(
            select(Team)
            .where(Team.id == team_id)
            .options(selectinload(Team.players))
        )

    async def delete_team(self, team_id: int) -> None:
        team = await self.session.get(Team, team_id)
        if team is None:
            raise UnknownTeamError(team_id)
        has_players = await self.session.scalar(
            select(Player.id).where(Player.team_id == team_id).limit(1)
        )
        if has_players:
            raise TeamNotEmptyError(team_id)
        await self.session.delete(team)
        await self.session.commit()

    async def get_players(
        self,
        team_id: int | None = None,
        position: Position | None = None,
        min_age: int | None = None,
    ) -> list[Player]:
        query = select(Player)
        if team_id is not None:
            query = query.where(Player.team_id == team_id)
        if position is not None:
            query = query.where(Player.position == position)
        if min_age is not None:
            query = query.where(Player.age >= min_age)
        result = await self.session.scalars(query)
        return list(result)

    async def create_player(
        self, name: str, age: int, position: Position, team_id: int | None = None
    ) -> Player:
        if team_id is not None:
            team = await self.session.get(Team, team_id)
            if team is None:
                raise UnknownTeamError(team_id)
        player = Player(name=name, age=age, position=position, team_id=team_id)
        self.session.add(player)
        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def get_player(self, player_id: int) -> Player | None:
        return await self.session.get(Player, player_id)

    async def add_player_to_team(self, player_id: int, team_id: int) -> Player:
        player = await self.session.get(Player, player_id)
        if player is None:
            raise UnknownPlayerError(player_id)
        team = await self.session.get(Team, team_id)
        if team is None:
            raise UnknownTeamError(team_id)
        player.team_id = team_id
        await self.session.commit()
        await self.session.refresh(player)
        return player

    async def remove_player_from_team(self, player_id: int) -> None:
        player = await self.session.get(Player, player_id)
        if player is None:
            raise UnknownPlayerError(player_id)
        player.team_id = None
        await self.session.commit()

    async def delete_player(self, player_id: int) -> None:
        player = await self.session.get(Player, player_id)
        if player is None:
            raise UnknownPlayerError(player_id)
        await self.session.delete(player)
        await self.session.commit()
