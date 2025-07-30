import unittest
import time
import HtmlTestRunner
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# =====================================================================================
# NOTA: Pentru a rula acest script, asigura-te ca:
# 1. Ai instalat librariile necesare: pip install selenium html-testRunner-pip
# 2. Ai descarcat ChromeDriver si este accesibil in sistem.
# =====================================================================================


# =====================================================================================
# CLASA 1: TEST PENTRU VALIDAREA FORMULARULUI DE INREGISTRARE
# =====================================================================================
class TestInregistrareHapiBeats(unittest.TestCase):
    def setUp(self):
        """Metoda de setup, ruleaza inainte de fiecare test din clasa."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://apps.qualiadept.eu/hapibeats/register.php")
        time.sleep(1)

    def test_validare_parola_nepotrivita(self):
        """Verifica mesajul de eroare cand parolele nu se potrivesc."""
        try:
            self.driver.find_element(By.ID, 'username').send_keys("testuser12345")
            self.driver.find_element(By.ID, 'firstName').send_keys("Test")
            self.driver.find_element(By.ID, 'lastName').send_keys("User")
            self.driver.find_element(By.ID, 'email').send_keys("test@user.com")
            self.driver.find_element(By.ID, 'email2').send_keys("test@user.com")
            self.driver.find_element(By.ID, 'password').send_keys("parola123")
            self.driver.find_element(By.ID, 'password2').send_keys("parola456")
            self.driver.find_element(By.NAME, 'registerButton').click()
            time.sleep(1)

            error_message = self.driver.find_element(By.CSS_SELECTOR, '#registerForm .errorMessage').text
            expected_error = "Your passwords don't match"
            self.assertEqual(error_message, expected_error,
                             f"Eroare: Mesajul afisat este '{error_message}', dar era asteptat '{expected_error}'")
        except NoSuchElementException as e:
            self.fail(f"Testul a esuat deoarece un element nu a fost gasit: {e}")

    def tearDown(self):
        """Metoda de teardown, ruleaza dupa fiecare test."""
        self.driver.quit()


# =====================================================================================
# CLASA 2: TEST PENTRU AUTENTIFICARE
# =====================================================================================
class TestAutentificareHapiBeats(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://apps.qualiadept.eu/hapibeats/register.php")
        time.sleep(1)

    def test_login_esuat(self):
        """Verifica mesajul de eroare la login cu date gresite."""
        try:
            self.driver.find_element(By.ID, 'loginUsername').send_keys("user_inexistent")
            self.driver.find_element(By.ID, 'loginPassword').send_keys("parolaGresita")
            self.driver.find_element(By.NAME, 'loginButton').click()
            time.sleep(1)

            error_message = self.driver.find_element(By.CSS_SELECTOR, '#loginForm .errorMessage').text
            expected_error = "Your username or password was incorrect"
            self.assertEqual(error_message, expected_error,
                             f"Eroare: Mesajul de login invalid este '{error_message}', dar era asteptat '{expected_error}'")
        except NoSuchElementException as e:
            self.fail(f"Testul a esuat deoarece un element nu a fost gasit: {e}")

    def test_login_reusit(self):
        """Verifica autentificarea cu un utilizator valid."""
        try:
            self.driver.find_element(By.ID, 'loginUsername').send_keys("george.datcu")
            self.driver.find_element(By.ID, 'loginPassword').send_keys("qazXSW13")
            self.driver.find_element(By.NAME, 'loginButton').click()

            # **CORECTIE**: Folosim o asteptare explicita in loc de time.sleep()
            # Asteptam maxim 10 secunde pana cand elementul cu clasa 'pageHeadingBig' devine vizibil
            wait = WebDriverWait(self.driver, 10)
            page_heading_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'pageHeadingBig')))

            page_heading = page_heading_element.text
            expected_heading = "You Might Also Like"
            self.assertEqual(page_heading, expected_heading, "Login-ul a esuat, nu am ajuns pe pagina principala.")
        except TimeoutException:
            self.fail("Testul a esuat: Pagina principala (Browse) nu s-a incarcat in timpul alocat.")
        except NoSuchElementException as e:
            self.fail(f"Testul a esuat deoarece un element nu a fost gasit: {e}")

    def tearDown(self):
        self.driver.quit()


# =====================================================================================
# CLASA 3: TEST PENTRU GESTIONAREA PLAYLIST-URILOR (ALERTA)
# =====================================================================================
class TestPlaylistManagement(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://apps.qualiadept.eu/hapibeats/register.php")
        time.sleep(1)
        self.driver.find_element(By.ID, 'loginUsername').send_keys("george.datcu")
        self.driver.find_element(By.ID, 'loginPassword').send_keys("qazXSW13")
        self.driver.find_element(By.NAME, 'loginButton').click()
        # Asteptam ca pagina sa se incarce dupa login
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pageHeadingBig')))

    def test_delete_playlist_alert(self):
        """Verifica crearea si stergerea unui playlist, inclusiv alerta de confirmare."""
        try:
            # **CORECTIE**: Folosim asteptari explicite pentru a face testul mai stabil
            wait = WebDriverWait(self.driver, 10)

            # Navigam la "Your Music"
            your_music_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[onclick*='yourMusic.php']")))
            your_music_link.click()

            # Apasam butonul "NEW PLAYLIST"
            new_playlist_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button.green')))
            new_playlist_button.click()

            # Asteptam si comutam pe alerta de tip prompt
            prompt_alert = wait.until(EC.alert_is_present())
            nume_playlist = f"Playlist Test {int(time.time())}"  # Nume unic pentru a evita conflicte
            prompt_alert.send_keys(nume_playlist)
            prompt_alert.accept()

            # Asteptam ca noul playlist sa apara in pagina si dam click pe el
            playlist_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{nume_playlist}']")))
            playlist_element.click()

            # Asteptam butonul de stergere si dam click
            delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='DELETE PLAYLIST']")))
            delete_button.click()

            # Asteptam si comutam pe alerta de confirmare
            confirm_alert = wait.until(EC.alert_is_present())

            expected_alert_text = "Are you sure you want to delte this playlist?"
            self.assertEqual(confirm_alert.text, expected_alert_text,
                             "Textul din alerta de stergere playlist nu este corect.")

            confirm_alert.accept()

            # Asteptam sa se reincarce pagina si verificam ca playlistul a disparut
            wait.until(EC.staleness_of(delete_button))  # Asteptam ca elementul vechi sa dispara
            self.assertNotIn(nume_playlist, self.driver.page_source, "Playlist-ul nu a fost sters cu succes.")

        except TimeoutException as e:
            self.fail(f"Testul a esuat din cauza unui timeout: {e}")
        except NoSuchElementException as e:
            self.fail(f"Testul a esuat deoarece un element nu a fost gasit: {e}")

    def tearDown(self):
        self.driver.quit()


# =====================================================================================
# CLASA 4: TEST PENTRU FUNCTIONALITATEA DE CAUTARE
# =====================================================================================
class TestSearchFunctionality(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://apps.qualiadept.eu/hapibeats/register.php")
        time.sleep(1)
        self.driver.find_element(By.ID, 'loginUsername').send_keys("george.datcu")
        self.driver.find_element(By.ID, 'loginPassword').send_keys("qazXSW13")
        self.driver.find_element(By.NAME, 'loginButton').click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pageHeadingBig')))

    def test_search_no_results(self):
        """Verifica mesajul afisat cand cautarea nu returneaza rezultate."""
        try:
            wait = WebDriverWait(self.driver, 10)

            # Navigam la pagina de cautare
            search_link = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".navItemLink[onclick*='search.php']")))
            search_link.click()

            # Asteptam sa apara campul de cautare si introducem text
            search_input = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'searchInput')))
            termen_inexistent = "qwertyuiopasdfghjkl"
            search_input.send_keys(termen_inexistent)

            # **CORECTIE**: Asteptam explicit sa apara mesajul, in loc de time.sleep()
            no_results_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'noResults')))

            no_songs_message = no_results_element.text
            expected_message = f"No songs found matching {termen_inexistent}"
            self.assertEqual(no_songs_message, expected_message, "Mesajul pentru nicio melodie gasita nu este corect.")
        except TimeoutException:
            self.fail("Testul a esuat: Mesajul 'No results' nu a aparut in timpul alocat.")
        except NoSuchElementException as e:
            self.fail(f"Testul a esuat deoarece un element nu a fost gasit: {e}")

    def tearDown(self):
        self.driver.quit()


# =====================================================================================
# BLOCUL PRINCIPAL DE EXECUTIE
# =====================================================================================
if __name__ == '__main__':
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTest(loader.loadTestsFromTestCase(TestInregistrareHapiBeats))
    suite.addTest(loader.loadTestsFromTestCase(TestAutentificareHapiBeats))
    suite.addTest(loader.loadTestsFromTestCase(TestPlaylistManagement))
    suite.addTest(loader.loadTestsFromTestCase(TestSearchFunctionality))

    reports_path = os.path.join(os.getcwd(), 'reports')

    runner = HtmlTestRunner.HTMLTestRunner(
        combine_reports=True,
        report_title="HapiBeats - Raport de Testare Automata",
        report_name="Rezultate Teste de Regresie",
        output=reports_path
    )

    runner.run(suite)
