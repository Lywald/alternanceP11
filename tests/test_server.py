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
def bookings_fixture():
    return [ {
      "club": "Pierre Club",
      "competition": "Pierre Festival",
      "places": 10
    } ]

@pytest.fixture
def client(competitions_fixture, clubs_fixture, bookings_fixture, monkeypatch):
    # Simulating a client
    monkeypatch.setattr('server.clubs', clubs_fixture)
    monkeypatch.setattr('server.competitions', competitions_fixture)
    monkeypatch.setattr('server.bookings', bookings_fixture)
    monkeypatch.setattr('server.saveClubs', lambda: None)
    monkeypatch.setattr('server.saveCompetitions', lambda: None)
    monkeypatch.setattr('server.saveBookings', lambda: None)
    return app.test_client()

def test_purchasePlaces_sad_invalid_competition(client, competitions_fixture, clubs_fixture):
    # User attempts a request with an unknown competition
    response = client.post('/purchasePlaces', data=dict(
        places='1',
        competition='Test invalide compétition',
        club='Pierre Club'
    ))
    assert b'Competition invalide' in response.data

def test_purchasePlaces_sad_invalid_club(client, competitions_fixture, clubs_fixture):
    # User attempts a request with an unknown club
    response = client.post('/purchasePlaces', data=dict(
        places='1',
        competition='Pierre Festival',
        club='Club invalide'
    ))
    assert b'Club invalide' in response.data

def test_purchasePlaces_happy_decount(client, competitions_fixture, clubs_fixture):
    # User buys places and updates their points
    assert int(competitions_fixture[0]['numberOfPlaces']) == 25
    assert int(clubs_fixture[0]['points']) == 10

    response = client.post('/purchasePlaces', data=dict(places=1, competition="Pierre Festival", club="Pierre Club"))
    #response = client.post('/purchasePlaces', data=dict(places=1, competition=competitions_fixture[0], club=clubs_fixture[0]))

    # Check the POST succeeded
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # Check points got deducted
    assert int(competitions_fixture[0]['numberOfPlaces']) == 24
    assert int(clubs_fixture[0]['points']) == 9

def test_purchasePlaces_sad_exceedingDozen(client, competitions_fixture, clubs_fixture, bookings_fixture):
    # Since we are booking more than a dozen in this competition, send a error message
    response = client.post('/purchasePlaces', data=dict(
        places='3',
        competition='Pierre Festival',
        club='Pierre Club'
    ))
    assert(response.status_code == 500)
    assert(b'Dozen places exceeded' in response.data)

def test_purchasePlaces_happy_underDozen(client, competitions_fixture, clubs_fixture, bookings_fixture):
    # Since we are booking less than a dozen total, then pass
    response = client.post('/purchasePlaces', data=dict(
        places='1',
        competition='Pierre Festival',
        club='Pierre Club'
    ))
    assert(response.status_code == 200)