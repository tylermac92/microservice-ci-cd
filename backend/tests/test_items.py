def test_create_item(client, token):
    response = client.post(
        "/items",
        json={"name": "Widget"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print("Status:", response.status_code)
    print("Body:", response.get_json())
    assert response.status_code == 201
    assert response.get_json()["name"] == "Widget"

def test_get_items(client, token):
    client.post("/items", json={"name": "Widget"}, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert any(item["name"] == "Widget" for item in response.get_json())
