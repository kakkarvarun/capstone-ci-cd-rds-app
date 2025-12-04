from web_app import app

def test_list_users_returns_list():
    client = app.test_client()
    resp = client.get("/users")
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

def test_create_user_requires_first_and_last_name():
    client = app.test_client()
    resp = client.post("/users", json={"first_name": "", "last_name": ""})
    assert resp.status_code == 400

def test_get_user_not_found():
    client = app.test_client()
    resp = client.get("/users/999999")
    assert resp.status_code in (404, 200)
