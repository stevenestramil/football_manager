from itertools import count
from core.models import Team, Player, Position


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
    def __init__(self):
        self._teams: dict[int, Team] = {}
        self._players: dict[int, Player] = {}
        self._team_ids = count(1)
        self._player_ids = count(1)

    def create_team(self, name: str, city: str, titles: int) -> Team:
        if any(t.name.lower() == name.lower() for t in self._teams.values()):
            raise DuplicateTeamNameError(name)
        team_id = next(self._team_ids)
        team = Team(id=team_id, name=name, city=city, titles=titles)
        self._teams[team_id] = team
        return team

    def get_teams(self) -> list[Team]:
        return list(self._teams.values())

    def get_team(self, team_id: int) -> Team | None:
        return self._teams.get(team_id)

    def delete_team(self, team_id: int) -> None:
        if team_id not in self._teams:
            raise UnknownTeamError(team_id)
        if any(p.team_id == team_id for p in self._players.values()):
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
        return player

    def get_player(self, player_id: int) -> Player | None:
        return self._players.get(player_id)

    def add_player_to_team(self, player_id: int, team_id: int) -> Player:
        player = self._players.get(player_id)
        if not player:
            raise UnknownPlayerError(player_id)
        if team_id not in self._teams:
            raise UnknownTeamError(team_id)
        player.team_id = team_id
        return player

    def remove_player_from_team(self, player_id: int) -> None:
        player = self._players.get(player_id)
        if not player:
            raise UnknownPlayerError(player_id)
        player.team_id = None

    def delete_player(self, player_id: int) -> None:
        if player_id not in self._players:
            raise UnknownPlayerError(player_id)
        del self._players[player_id]
