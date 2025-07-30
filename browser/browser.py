# Fisier: browser/browser.py
from selenium import webdriver

class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # Am scos implicit_wait de aici pentru a ne baza exclusiv pe asteptari explicite,
        # care sunt mai sigure si mai flexibile.
    def close(self):
        self.driver.quit()