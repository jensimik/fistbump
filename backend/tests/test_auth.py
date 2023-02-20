def test_auth(client):
    me = client.get("/auth/me")
    assert me.status_code == 401

    register = client.post("/auth/register")
    assert register.status_code == 200
    access_token = register.json()["access_token"]
    assert access_token is not None

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me.status_code == 200
    assert "uuid" in me.json()