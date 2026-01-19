from server import app
from server import loadCompetitions
from server import loadClubs
from server import purchasePlaces
import pytest

@pytest.fixture
def client(monkeypatch):
    return app.test_client()

def test_showSummary_sad_invalid(client):    
    with pytest.raises(IndexError):
        response = client.post('/showSummary', data=dict(email='inconnu@test.com'))
        # assert(response.status_code == 500)

def test_showSummary_happy_valid(client):
    response = client.post('/showSummary', data=dict(email='admin@irontemple.com'))
    assert(response.status_code == 200)