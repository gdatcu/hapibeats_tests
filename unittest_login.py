import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Planul de construcție pentru testele de Login
class TestLoginHapiBeats(unittest.TestCase):

    # Linia de asamblare: rulează înaintea fiecărui test
    def setUp(self):
        # Pornește motorul Chrome
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Navighează la pagina de start
        # ATENȚIE: Înlocuiește cu calea absolută de pe computerul tău!
        self.driver.get(
            "https://apps.qualiadept.eu/hapibeats/register.php")
        time.sleep(1)

    # Testul #1: Login cu credențiale valide
    def test_login_cu_credentiale_valide(self):
        # Pas 1: Introdu numele de utilizator
        self.driver.find_element(By.ID, "loginUsername").send_keys("george.datcu")

        # Pas 2: Introdu parola
        # Din SQL, știm că parola pentru 'george.datcu' este 'qazXSW13'
        self.driver.find_element(By.ID, "loginPassword").send_keys("qazXSW@13")

        # Pas 3: Apasă butonul de Login
        self.driver.find_element(By.NAME, "loginButton").click()
        time.sleep(2)  # Așteaptă redirectarea

        # Pas 4: Verificarea finală! Am ajuns unde trebuie?
        # Căutăm un element care există DOAR după login (ex: bara de navigare).
        try:
            self.driver.find_element(By.ID, "navBarContainer")
            login_reusit = True
        except:
            login_reusit = False

        # Afirmă rezultatul așteptat
        self.assertTrue(login_reusit, "Verificare eșuată: Login-ul nu a avut succes, navBarContainer nu a fost găsit.")

        # Testul #2: Login cu credențiale valide
    def test_login_cu_credentiale_invalide(self):
            # Pas 1: Introdu numele de utilizator
            self.driver.find_element(By.ID, "loginUsername").send_keys("george.datcu")

            # Pas 2: Introdu parola
            # Din SQL, știm că parola pentru 'reece-kenney' este 'password'
            self.driver.find_element(By.ID, "loginPassword").send_keys("qazXSW13")

            # Pas 3: Apasă butonul de Login
            self.driver.find_element(By.NAME, "loginButton").click()
            time.sleep(2)  # Așteaptă redirectarea

            # Pas 4: Verificarea finală! Am ajuns unde trebuie?
            # Căutăm un element care există DOAR după login (ex: bara de navigare).
            try:
                self.driver.find_element(By.ID, "navBarContainer")
                login_reusit = True
            except:
                login_reusit = False

            # Afirmă rezultatul așteptat
            self.assertFalse(login_reusit,
                            "Verificare eșuată: Login-ul nu ar fi trebuit sa se intample. Avem o bresa de securitate!")

    # Dezasamblarea: rulează după fiecare test
    def tearDown(self):
        # Închide browser-ul pentru a elibera resursele
        self.driver.quit()


# Punctul de start pentru rularea testelor
if __name__ == "__main__":
    unittest.main(verbosity=2)
