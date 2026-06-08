from core.storage import Storage
from core.models import Player, Position


class PlayerService:
    def __init__(self, storage: Storage):
        self.storage: Storage = storage

    def get_players(
        self,
        team_id: int | None = None,
        position: Position | None = None,
        min_age: int | None = None,
    ) -> list[Player]:
        return self.storage.get_players(team_id=team_id, position=position, min_age=min_age)

    def create_player(
        self, name: str, age: int, position: Position, team_id: int | None = None
    ) -> Player:
        return self.storage.create_player(
            name=name,
            age=age,
            position=position,
            team_id=team_id,
        )

    def get_player(self, player_id: int) -> Player | None:
        return self.storage.get_player(player_id=player_id)

    def assign_player_to_team(self, player_id: int, team_id: int) -> Player:
        return self.storage.add_player_to_team(player_id=player_id, team_id=team_id)

    def remove_player_from_team(self, player_id: int) -> None:
        self.storage.remove_player_from_team(player_id)

    def delete_player(self, player_id: int) -> None:
        self.storage.delete_player(player_id)
