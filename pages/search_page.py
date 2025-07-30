# Fisier: pages/search_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchPage(BasePage):
    SEARCH_LINK = (By.CSS_SELECTOR, ".navItemLink[onclick*='search.php']")
    SEARCH_INPUT = (By.CLASS_NAME, 'searchInput')
    RESULTS_CONTAINER = (By.CLASS_NAME, 'tracklistContainer')
    NO_RESULTS_MESSAGE = (By.CLASS_NAME, 'noResults')

    def navigheaza_la_cautare(self): self.wait_and_click_element(self.SEARCH_LINK)
    def introdu_termen_cautare(self, t): self.send_keys_to_element(self.SEARCH_INPUT, t)
    def verifica_existenta_rezultatelor(self): assert self.is_element_displayed(self.RESULTS_CONTAINER)
    def verifica_mesaj_fara_rezultate(self, t):
        expected = f"No songs found matching {t}"
        actual = self.get_element_text(self.NO_RESULTS_MESSAGE)
        assert actual == expected
