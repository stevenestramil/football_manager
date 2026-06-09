from core.storage import Storage
from core.models import Team


class TeamService:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def create_team(self, name: str, city: str, titles: int) -> Team:
        return await self.storage.create_team(name=name, city=city, titles=titles)

    async def get_teams(self) -> list[Team]:
        return await self.storage.get_teams()

    async def get_team(self, team_id: int) -> Team | None:
        return await self.storage.get_team(team_id)

    async def delete_team(self, team_id: int) -> None:
        await self.storage.delete_team(team_id)
