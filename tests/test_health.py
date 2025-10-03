from app import create_app

def test_health():
    app = create_app()
    client = app.test_client()
    assert client.get("/healthz").status_code == 200
