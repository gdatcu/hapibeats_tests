import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestSearchHapiBeats(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://apps.qualiadept.eu/hapibeats/register.php")
        time.sleep(1)

        # Pre-condiție: Login înainte de a putea căuta
        self.driver.find_element(By.ID, "loginUsername").send_keys("george.datcu")
        self.driver.find_element(By.ID, "loginPassword").send_keys("qazXSW13")
        self.driver.find_element(By.NAME, "loginButton").click()
        time.sleep(2)

    def test_cautare_melodie_existenta(self):
        # Pas 1: Accesează pagina de căutare
        self.driver.find_element(By.CSS_SELECTOR, ".navItemLink[onclick*='search.php']").click()
        time.sleep(1)

        # Pas 2: Introdu termenul de căutare
        search_input = self.driver.find_element(By.CLASS_NAME, "searchInput")
        search_input.send_keys("Happy Rock")

        # Pas 3: Așteaptă ca AJAX să returneze rezultatele (scriptul are un delay de 2s)
        time.sleep(2.5)

        # Pas 4: Verifică dacă melodia apare în listă
        lista_melodii_gasite = self.driver.find_elements(By.CLASS_NAME, "trackName")

        # Extrage textul din elementele web
        nume_melodii = [melodie.text for melodie in lista_melodii_gasite]
        print(f"Afiseaza numele melodiilor: ${nume_melodii}")

        # Afirmă că melodia căutată se află în lista de rezultate
        self.assertIn("Living my life", nume_melodii, "Verificare eșuată: Melodia 'Happy Rock' nu a apărut în rezultate.")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
