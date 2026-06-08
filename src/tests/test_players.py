def test_create_player(client, created_team):
    response = client.post(
        "/players",
        json={"name": "John Doe", "age": 25, "position": "midfielder", "team_id": created_team["id"]},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"


def test_create_player_invalid_position(client, created_team):
    response = client.post(
        "/players",
        json={"name": "John Doe", "age": 25, "position": "striker", "team_id": created_team["id"]},
    )
    assert response.status_code == 422


def test_create_player_invalid_team(client):
    response = client.post(
        "/players",
        json={"name": "John Doe", "age": 25, "position": "midfielder", "team_id": 999},
    )
    assert response.status_code == 404


def test_assign_player_to_team(client, created_team):
    player = client.post(
        "/players",
        json={"name": "John Doe", "age": 25, "position": "midfielder"},
    ).json()

    response = client.patch(
        f"/players/{player['id']}/team",
        json={"team_id": created_team["id"]},
    )
    assert response.status_code == 200


def test_assign_player_to_nonexistent_team(client, created_team):
    player = client.post(
        "/players",
        json={"name": "John Doe", "age": 25, "position": "midfielder"},
    ).json()

    response = client.patch(
        f"/players/{player['id']}/team",
        json={"team_id": 999},
    )
    assert response.status_code == 404
