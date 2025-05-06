def test_register(client):
    response = client.post("/auth/register", json={"username": "alice", "password": "secret"})
    assert response.status_code == 200 or response.status_code == 201

def test_login(client):
    client.post("/auth/register", json={"username": "bob", "password": "pass"})
    response = client.post("/auth/login", json={"username": "bob", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.get_json()
