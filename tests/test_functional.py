import pytest
import shutil
from server import app


DATA_FILES = ['clubs.json', 'competitions.json', 'bookings.json']


@pytest.fixture
def backup_data():
    """Sauvegarde et restaure les fichiers JSON pour ne pas altérer les données."""
    for f in DATA_FILES:
        shutil.copy(f, f + '.bak')
    yield
    for f in DATA_FILES:
        shutil.copy(f + '.bak', f)
        shutil.os.remove(f + '.bak')


@pytest.fixture
def client():
    return app.test_client()


def test_full_booking_workflow(client, backup_data):
    """Scénario complet: login -> voir compétitions -> réserver -> vérifier mise à jour."""

    # 1. Login avec un email valide
    response = client.post('/showSummary',
        data=dict(email='kate@shelifts.co.uk'),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in response.data
    assert b'Future Comp' in response.data

    # 2. Accéder à la page de réservation d'une compétition future
    response = client.get('/book/Future%20Comp/She%20Lifts')
    assert response.status_code == 200
    assert b'Booking for' in response.data
    assert b'How many places?' in response.data

    # 3. Réserver 2 places
    response = client.post('/purchasePlaces', data=dict(
        places='2',
        competition='Future Comp',
        club='She Lifts'
    ))
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data

    # 4. Vérifier que les points ont été déduits (12 - 2 = 10)
    assert b'Points available: 10' in response.data

    # 5. Vérifier que les places de la compétition ont diminué (18 - 2 = 16)
    assert b'Number of Places: 16' in response.data
