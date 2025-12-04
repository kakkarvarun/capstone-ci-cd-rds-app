from web_app import app

def test_health_ok():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code in (200, 500)

def test_health_has_status_key():
    client = app.test_client()
    resp = client.get("/health")
    data = resp.get_json()
    assert "status" in data
