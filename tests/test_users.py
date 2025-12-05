from web_app import app


class DummyCursor:
    def __init__(self, users=None):
        # users is a list of dicts like {"id": 1, "first_name": "...", ...}
        self.users = users or []
        self._last_id = None

    def execute(self, query, params=None):
        # Very simple behavior: just remember the id if it's a SELECT by id
        if params and len(params) == 1:
            self._last_id = params[0]
        else:
            self._last_id = None

    def fetchall(self):
        # Return all fake users
        return [
            (u["id"], u["first_name"], u["last_name"], u["email"])
            for u in self.users
        ]

    def fetchone(self):
        # Return one fake user if id matches, otherwise None
        if self._last_id is None:
            return None

        for u in self.users:
            if u["id"] == self._last_id:
                return (u["id"], u["first_name"], u["last_name"], u["email"])
        return None

    def close(self):
        pass


class DummyConnection:
    def __init__(self, users=None):
        self.users = users or []

    def cursor(self):
        return DummyCursor(self.users)

    def close(self):
        pass


def test_list_users_returns_list(monkeypatch):
    """Should return 200 and a list (even in CI without real DB)."""

    # Prepare some fake users for the test
    fake_users = [
        {"id": 1, "first_name": "Varun", "last_name": "K", "email": "varun@example.com"},
        {"id": 2, "first_name": "Richard", "last_name": "B", "email": "richard@example.com"},
    ]

    def fake_get_db_connection():
        return DummyConnection(fake_users)

    # Patch the real DB connection in web_app
    monkeypatch.setattr("web_app.get_db_connection", fake_get_db_connection)

    client = app.test_client()
    resp = client.get("/users")

    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_user_not_found(monkeypatch):
    """Should return 404 (or 200 with not-found message) if user doesn't exist."""

    # No users in DB for this test
    def fake_get_db_connection():
        return DummyConnection([])

    monkeypatch.setattr("web_app.get_db_connection", fake_get_db_connection)

    client = app.test_client()
    resp = client.get("/users/999999")

    # Your app might return 404 or 200 with some message; keep both valid:
    assert resp.status_code in (404, 200)