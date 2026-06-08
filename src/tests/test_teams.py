def test_create_team(client):
    response = client.post("/teams", json={"name": "Arsenal", "city": "London", "titles": 13})
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Arsenal"
    assert "players" not in body


def test_create_team_invalid_name(client):
    response = client.post("/teams", json={"name": "AB", "city": "London", "titles": 0})
    assert response.status_code == 422


def test_get_teams_empty(client):
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []


def test_get_teams(client, created_team):
    response = client.get("/teams")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_team(client, created_team):
    response = client.get(f"/teams/{created_team['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Arsenal"


def test_get_team_not_found(client):
    response = client.get("/teams/999")
    assert response.status_code == 404


def test_delete_team(client, created_team):
    response = client.delete(f"/teams/{created_team['id']}")
    assert response.status_code == 204


def test_delete_team_not_found(client):
    response = client.delete("/teams/999")
    assert response.status_code == 404

def test_delete_team_with_players(client, created_team):
    # Create a player assigned to the team
    player_response = client.post(
        "/players",
        json={"name": "John Doe", "age": 25, "position": "midfielder", "team_id": created_team["id"]},
    )
    assert player_response.status_code == 201

    # Attempt to delete the team
    response = client.delete(f"/teams/{created_team['id']}")
    assert response.status_code == 400