# Fisier: browser/browser.py

from selenium import webdriver

class Browser:
    """
    Aceasta clasa este responsabila exclusiv pentru
    initializarea si inchiderea driver-ului de browser.
    Este "cheia de contact" a framework-ului nostru.
    """
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.implicitly_wait(5) # O asteptare implicita generala

    def close(self):
        self.driver.quit()
