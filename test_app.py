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