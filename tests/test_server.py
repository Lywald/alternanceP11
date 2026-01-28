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