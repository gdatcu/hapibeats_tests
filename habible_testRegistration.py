# script_inregistrare_succes.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid  # Pentru a genera nume de utilizator și email-uri unice


def test_user_registration_success():
    # Inițializarea driver-ului Chrome. Asigură-te că chromedriver este în PATH.
    driver = webdriver.Chrome()
    driver.get("https://apps.qualiadept.eu/hapibeats/register.php")
    driver.maximize_window()  # Maximizează fereastra browser-ului

    try:
        # Așteaptă până când elementul "hideLogin" este clickabil și apoi dă click
        # Acest element comută vizibilitatea formularelor de login/înregistrare
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "hideLogin"))
        ).click()

        # Generare date unice pentru a evita conflictele la înregistrare
        unique_id = str(uuid.uuid4())[:8]  # Un ID scurt și unic
        username = f"testuser_{unique_id}"
        email = f"test_{unique_id}@example.com"

        # Completează formularul de înregistrare cu date valide
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "firstName").send_keys("PrenumeTest")
        driver.find_element(By.ID, "lastName").send_keys("NumeTest")
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "email2").send_keys(email)
        driver.find_element(By.ID, "password").send_keys("Parola123!")
        driver.find_element(By.ID, "password2").send_keys("Parola123!")

        # Click pe butonul de înregistrare
        driver.find_element(By.NAME, "registerButton").click()

        # Așteaptă redirecționarea către pagina principală (index.php sau browse.php)
        # Verifică dacă URL-ul conține "index.php" sau "browse.php"
        WebDriverWait(driver, 10).until(
            EC.url_contains("index.php") or EC.url_contains("browse.php")
        )

        # Verifică dacă utilizatorul este logat, căutând un element specific de pe pagina principală
        # De exemplu, prezența elementului cu ID-ul "mainContainer"
        assert driver.find_element(By.ID, "mainContainer").is_displayed()
        print(f"Test de înregistrare reușit pentru utilizatorul: {username}")

    except Exception as e:
        print(f"Test de înregistrare eșuat: {e}")
        driver.save_screenshot("registration_failure.png")  # Salvează un screenshot în caz de eșec
    finally:
        driver.quit()  # Închide browser-ul

# Pentru a rula testul, decomentează linia de mai jos:
# test_user_registration_success()
