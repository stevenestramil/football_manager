from itertools import count
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from core.models import Team, Player, Position
from core.db_models import TeamORM


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
    def __init__(self, session: Session):
        self.session = session
        self._teams: dict[int, Team] = {}
        self._players: dict[int, Player] = {}
        self._team_ids = count(1)
        self._player_ids = count(1)

    def create_team(self, name: str, city: str, titles: int) -> TeamORM:
        existing = self.session.scalar(
            select(TeamORM).where(func.lower(TeamORM.name) == name.lower())
        )
        if existing is not None:
            raise DuplicateTeamNameError(name)
        team = TeamORM(name=name, city=city, titles=titles)
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team

    def get_teams(self) -> list[Team]:
        return list(self._teams.values())

    def get_team(self, team_id: int) -> Team | None:
        return self._teams.get(team_id)

    def delete_team(self, team_id: int) -> None:
        team = self._teams.get(team_id)
        if team is None:
            raise UnknownTeamError(team_id)
        if team.players:
            raise TeamNotEmptyError(team_id)
        del self._teams[team_id]

    def get_players(
        self,
        team_id: int | None = None,
        position: Position | None = None,
        min_age: int | None = None,
    ) -> list[Player]:
        players = self._players.values()
        if team_id is not None:
            players = filter(lambda p: p.team_id == team_id, players)
        if position is not None:
            players = filter(lambda p: p.position == position, players)
        if min_age is not None:
            players = filter(lambda p: p.age >= min_age, players)
        return list(players)

    def create_player(
        self, name: str, age: int, position: Position, team_id: int | None = None
    ) -> Player:
        if team_id is not None and team_id not in self._teams:
            raise UnknownTeamError(team_id)
        player_id = next(self._player_ids)
        player = Player(id=player_id, name=name, age=age, position=position, team_id=team_id)
        self._players[player_id] = player
        if team_id is not None:
            self._teams[team_id].players.append(player_id)
        return player

    def get_player(self, player_id: int) -> Player | None:
        return self._players.get(player_id)

    def add_player_to_team(self, player_id: int, team_id: int) -> Player:
        player = self._players.get(player_id)
        if not player:
            raise UnknownPlayerError(player_id)
        if team_id not in self._teams:
            raise UnknownTeamError(team_id)
        if player.team_id is not None:
            self._teams[player.team_id].players.remove(player_id)
        player.team_id = team_id
        self._teams[team_id].players.append(player_id)
        return player

    def remove_player_from_team(self, player_id: int) -> None:
        player = self._players.get(player_id)
        if not player:
            raise UnknownPlayerError(player_id)
        if player.team_id is None:
            return
        self._teams[player.team_id].players.remove(player_id)
        player.team_id = None

    def delete_player(self, player_id: int) -> None:
        player = self._players.get(player_id)
        if not player:
            raise UnknownPlayerError(player_id)
        if player.team_id is not None:
            self._teams[player.team_id].players.remove(player_id)
        del self._players[player_id]
