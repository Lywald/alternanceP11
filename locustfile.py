# locustfile.py
from locust import HttpUser, task, between

class GudliftUser(HttpUser):
    # Chaque utilisateur attend 1-3 secondes entre chaque action
    wait_time = between(1, 3)

    @task
    def login(self):
        self.client.post('/showSummary', data=dict(
            email='admin@irontemple.com'
        ))

    @task
    def purchase_places(self):
        self.client.post('/purchasePlaces', data=dict(
            places='1',
            competition='Spring Festival',
            club='Iron Temple'
        ))

    @task
    def display_board(self):
        self.client.get('/points')