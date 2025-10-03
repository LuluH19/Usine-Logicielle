from app import create_app

def test_login_ok():
    app = create_app()
    client = app.test_client()
    r = client.post("/auth/login", json={"username":"alice","password":"alice123"})
    assert r.status_code == 200
    assert "token" in r.get_json()
