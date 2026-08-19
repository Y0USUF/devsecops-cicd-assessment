import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_home(client):
    """Test that home page returns 200 OK and expected text."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"DevSecOps Pipeline" in rv.data

def test_health(client):
    """Test that health check returns status: healthy."""
    rv = client.get('/health')
    assert rv.status_code == 404
    json_data = rv.get_json()
    assert json_data['status'] == 'healthy'
