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
    }, {
        "name": "Future Festival",
        "date": "2027-01-01 10:00:00",
        "numberOfPlaces": "22"
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
    monkeypatch.setattr('server.clubs', clubs_fixture)
    monkeypatch.setattr('server.competitions', competitions_fixture)
    monkeypatch.setattr('server.saveClubs', lambda: None)
    monkeypatch.setattr('server.saveCompetitions', lambda: None)
    return app.test_client()

def test_booking_past_competition(client, competitions_fixture, clubs_fixture):
    # Past competitions are rejected
    response = client.get('/book/' + competitions_fixture[0]["name"] + "/" + clubs_fixture[0]["name"])
    assert(response.status_code == 200)
    assert(b"Competition is past" in response.data)

def test_booking_future_competition(client, competitions_fixture, clubs_fixture):
    # Future competitions are booked successfully
    response = client.get('/book/' + competitions_fixture[1]["name"] + "/" + clubs_fixture[0]["name"])
    assert(response.status_code == 200)
    
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
