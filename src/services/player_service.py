from core.db_models import PlayerORM
from core.enums import Position
from core.storage import Storage


class PlayerService:
    def __init__(self, storage: Storage):
        self.storage: Storage = storage

    async def get_players(
        self,
        team_id: int | None = None,
        position: Position | None = None,
        min_age: int | None = None,
    ) -> list[PlayerORM]:
        return await self.storage.get_players(team_id=team_id, position=position, min_age=min_age)

    async def create_player(
        self, name: str, age: int, position: Position, team_id: int | None = None
    ) -> PlayerORM:
        return await self.storage.create_player(
            name=name,
            age=age,
            position=position,
            team_id=team_id,
        )

    async def get_player(self, player_id: int) -> PlayerORM | None:
        return await self.storage.get_player(player_id=player_id)

    async def assign_player_to_team(self, player_id: int, team_id: int) -> PlayerORM:
        return await self.storage.add_player_to_team(player_id=player_id, team_id=team_id)

    async def remove_player_from_team(self, player_id: int) -> None:
        await self.storage.remove_player_from_team(player_id)

    async def delete_player(self, player_id: int) -> None:
        await self.storage.delete_player(player_id)
