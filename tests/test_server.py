from server import app
from server import loadCompetitions
from server import loadClubs
from server import purchasePlaces
import pytest

@pytest.fixture
def client(monkeypatch):
    # Test client for requests
    return app.test_client()

def test_showSummary_sad_invalid(client):    
    # Login attempt with invalid email
    response = client.post('/showSummary', data=dict(email='inconnu@test.com'))
    assert(response.status_code == 500)
    assert b'Email invalide' in response.data

def test_showSummary_happy_valid(client):
    # Login attempt with valid email
    response = client.post('/showSummary', data=dict(email='admin@irontemple.com'))
    assert(response.status_code == 200)