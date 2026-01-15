import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test the observability health endpoint."""
    rv = client.get('/devops/health')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert 'status' in json_data
    assert 'version' in json_data

def test_metrics_endpoint(client):
    """Test that metrics endpoint returns prometheus data."""
    rv = client.get('/devops/metrics')
    assert rv.status_code == 200
    assert b'app_version_info' in rv.data

def test_home_redirect(client):
    """Test that home redirects to login."""
    rv = client.get('/', follow_redirects=True)
    assert rv.status_code == 200
    assert b'Sign In' in rv.data
