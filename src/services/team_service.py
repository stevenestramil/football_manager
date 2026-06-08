# src/services/team_service.py
from core.storage import Storage
from core.models import Team


class TeamService:
    def __init__(self, storage: Storage):
        self.storage = storage

    def create_team(self, name: str, city: str, titles: int) -> Team:
        return self.storage.create_team(
            name=name,
            city=city,
            titles=titles,
        )

    def get_teams(self) -> list[Team]:
        return self.storage.get_teams()

    def get_team(self, team_id: int) -> Team | None:
        return self.storage.get_team(team_id)

    def delete_team(self, team_id: int) -> None:
        self.storage.delete_team(team_id)
