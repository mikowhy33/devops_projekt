import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test endpointu /"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Czesc!" in rv.data

def test_products(client):
    """Test endpointu /products"""
    rv = client.get('/products')
    assert rv.status_code == 200
    assert b"Laptop" in rv.data

def test_version(client):
    """Test endpointu /version"""
    rv = client.get('/version')
    assert rv.status_code == 200
    # JSON should contain a 'version' key
    assert b"version" in rv.data

def test_health(client):
    """Test endpointu /health"""
    rv = client.get('/health')
    assert rv.status_code == 200
    assert b"OK" in rv.data