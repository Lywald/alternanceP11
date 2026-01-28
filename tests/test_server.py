from server import app
from server import loadCompetitions
from server import loadClubs
from server import purchasePlaces
import pytest

"""
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

def test_purchasePlaces(competitions_fixture, clubs_fixture):
    # Test purchasing places
    print("test_purchasePlaces")
    
    assert int(competitions_fixture[0]['numberOfPlaces']) == 25
    assert int(clubs_fixture[0]['points']) == 10

    # app.competitions = competitions_fixture
    # app.clubs = clubs_fixture
    with app.test_client() as client:
        response = client.post('/purchasePlaces', data=dict(places=1, competition="Pierre Festival", club="Pierre Club"))
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        assert int(competitions_fixture[0]['numberOfPlaces']) == 24
        assert int(clubs_fixture[0]['points']) == 9

        print(competitions_fixture[0]['numberOfPlaces'])
        print(clubs_fixture[0]['points'])

        assert int(competitions_fixture[0]['numberOfPlaces']) == 24
        assert int(clubs_fixture[0]['points']) == 9

"""

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

def test_booking_past_happy_valid(client, competitions_fixture, clubs_fixture):
    response = client.get('/book/' + competitions_fixture[0]["name"] + "/" + clubs_fixture[0]["name"])
    assert(response.status_code == 200)
    #with pytest.raises(IndexError):
    #    response = client.post('/showSummary', data=dict(email='inconnu@test.com'))
        # assert(response.status_code == 500)

def test_booking_past_happy_invalid(client, competitions_fixture, clubs_fixture):
    response = client.get('/book/' + competitions_fixture[1]["name"] + "/" + clubs_fixture[0]["name"])
    assert(response.status_code == 500)