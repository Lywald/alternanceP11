from server import app
from server import loadCompetitions
from server import loadClubs
from server import purchasePlaces
import pytest

@pytest.fixture
def competitions_fixture():
    return [ {
        "name": "Pierre Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    } ]

@pytest.fixture
def clubs_fixture():
    return [ {
        "name": "Pierre Club",
        "email": "pierre@pierre.com",
        "points": "10"
    } ]

@pytest.fixture
def client(competitions_fixture, clubs_fixture, monkeypatch):
    # Simulating a client
    monkeypatch.setattr('server.clubs', clubs_fixture)
    monkeypatch.setattr('server.competitions', competitions_fixture)
    return app.test_client()

def test_purchasePlaces_sad_invalid_competition(client, competitions_fixture, clubs_fixture):
    # L'utilisateur tente une requête avec une compétition inconnue
    response = client.post('/purchasePlaces', data=dict(
        places='1',
        competition='Test invalide compétition',
        club='Pierre Club'
    ))
    assert b'Competition invalide' in response.data

def test_purchasePlaces_sad_invalid_club(client, competitions_fixture, clubs_fixture):
    # L'utilisateur tente une requête avec un club inconnue
    response = client.post('/purchasePlaces', data=dict(
        places='1',
        competition='Pierre Festival',
        club='Club invalide'
    ))
    assert b'Club invalide' in response.data

def test_purchasePlaces_happy(client, competitions_fixture, clubs_fixture):
    # L'utilisateur achète des places, et on met à jour ses points    
    assert int(competitions_fixture[0]['numberOfPlaces']) == 25
    assert int(clubs_fixture[0]['points']) == 10

    # with app.test_client() as client:
    response = client.post('/purchasePlaces', data=dict(places=1, competition="Pierre Festival", club="Pierre Club"))
    
    # Check the POST succeeded
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Check points got deducted
    assert int(competitions_fixture[0]['numberOfPlaces']) == 24
    assert int(clubs_fixture[0]['points']) == 9