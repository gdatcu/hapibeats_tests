# Fisier: pages/login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://apps.qualiadept.eu/hapibeats/register.php"
    USERNAME_INPUT = (By.ID, 'loginUsername')
    PASSWORD_INPUT = (By.ID, 'loginPassword')
    LOGIN_BUTTON = (By.NAME, 'loginButton')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '#loginForm .errorMessage')
    PAGE_HEADING = (By.CLASS_NAME, 'pageHeadingBig')

    def load(self): self.driver.get(self.URL)
    def introdu_username(self, u): self.send_keys_to_element(self.USERNAME_INPUT, u)
    def introdu_parola(self, p): self.send_keys_to_element(self.PASSWORD_INPUT, p)
    def apas_buton_login(self): self.wait_and_click_element(self.LOGIN_BUTTON)
    def verifica_mesaj_eroare(self, txt): assert self.get_element_text(self.ERROR_MESSAGE) == txt
    def verifica_login_reusit(self, txt): assert self.get_element_text(self.PAGE_HEADING) == txt
