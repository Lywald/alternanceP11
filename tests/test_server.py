from server import app
from server import loadCompetitions
from server import loadClubs
from server import purchasePlaces
import pytest

@pytest.fixture
def client(monkeypatch):
    # Client de test pour requêtes
    return app.test_client()

def test_showSummary_sad_invalid(client):    
    # Tentative de connexion par une email invalide
    response = client.post('/showSummary', data=dict(email='inconnu@test.com'))
    assert(response.status_code == 500)
    assert b'Email invalide' in response.data

def test_showSummary_happy_valid(client):
    # Tentative de connexion par une email valide
    response = client.post('/showSummary', data=dict(email='admin@irontemple.com'))
    assert(response.status_code == 200)