import pytest
import threading
import time
import shutil
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from server import app


DATA_FILES = ['clubs.json', 'competitions.json', 'bookings.json']


@pytest.fixture(scope="module")
def live_server():
    """Lance le serveur Flask dans un thread séparé."""
    server = threading.Thread(
        target=lambda: app.run(port=5000, use_reloader=False)
    )
    server.daemon = True
    server.start()
    # Attendre que le serveur soit prêt
    for _ in range(10):
        try:
            urllib.request.urlopen("http://localhost:5000/")
            break
        except Exception:
            time.sleep(0.5)
    yield "http://localhost:5000"


@pytest.fixture(scope="module")
def backup_data():
    """Sauvegarde et restaure les fichiers JSON pour ne pas altérer les données."""
    for f in DATA_FILES:
        shutil.copy(f, f + '.bak')
    yield
    for f in DATA_FILES:
        shutil.copy(f + '.bak', f)
        shutil.os.remove(f + '.bak')


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def login(browser, base_url, email):
    """Helper: se connecter via le formulaire index."""
    browser.get(base_url)
    email_input = browser.find_element(By.NAME, "email")
    email_input.send_keys(email)
    email_input.submit()


def test_login_valid_email(live_server, backup_data, browser):
    """Un utilisateur se connecte avec un email valide et voit la page welcome."""
    login(browser, live_server, "kate@shelifts.co.uk")

    WebDriverWait(browser, 5).until(EC.title_contains("Summary"))
    assert "Welcome, kate@shelifts.co.uk" in browser.page_source


def test_login_invalid_email(live_server, backup_data, browser):
    """Un utilisateur se connecte avec un email invalide et voit un message d'erreur."""
    login(browser, live_server, "fake@email.com")

    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "flashes"))
    )
    assert "Email invalide" in browser.page_source


def test_book_places_on_future_competition(live_server, backup_data, browser):
    """Un utilisateur réserve des places sur une compétition future."""
    login(browser, live_server, "kate@shelifts.co.uk")
    WebDriverWait(browser, 5).until(EC.title_contains("Summary"))

    # Cliquer sur "Book Places" pour Future Comp (seule compétition future avec des places)
    links = browser.find_elements(By.LINK_TEXT, "Book Places")
    links[-1].click()

    WebDriverWait(browser, 5).until(EC.title_contains("Booking for"))

    # Réserver 1 place
    places_input = browser.find_element(By.NAME, "places")
    places_input.send_keys("1")
    places_input.submit()

    WebDriverWait(browser, 5).until(EC.title_contains("Summary"))
    assert "Great-booking complete!" in browser.page_source


def test_book_past_competition(live_server, backup_data, browser):
    """Un utilisateur tente de réserver sur une compétition passée et reçoit une erreur."""
    browser.get(live_server + "/book/Spring%20Festival/She%20Lifts")

    WebDriverWait(browser, 5).until(EC.title_contains("Summary"))
    assert "Competition is past" in browser.page_source


def test_points_display(live_server, backup_data, browser):
    """La page points affiche tous les clubs et leurs points."""
    browser.get(live_server + "/points")

    WebDriverWait(browser, 5).until(EC.title_contains("Points"))
    assert "Simply Lift" in browser.page_source
    assert "Iron Temple" in browser.page_source
    assert "She Lifts" in browser.page_source


def test_logout(live_server, backup_data, browser):
    """Un utilisateur se déconnecte et revient à la page d'accueil."""
    login(browser, live_server, "kate@shelifts.co.uk")
    WebDriverWait(browser, 5).until(EC.title_contains("Summary"))

    browser.find_element(By.LINK_TEXT, "Logout").click()

    WebDriverWait(browser, 5).until(EC.title_contains("GUDLFT Registration"))
