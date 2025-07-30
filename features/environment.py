# Fisier: features/environment.py
from browser.browser import Browser
from pages.login_page import LoginPage
from pages.search_page import SearchPage

def before_all(context):
    print("🎬 PREGATIREA PLATOURILOR DE FILMARE...")
    context.browser = Browser()
    context.login_page = LoginPage(context.browser.driver)
    context.search_page = SearchPage(context.browser.driver)

def after_all(context):
    if hasattr(context, 'browser'):
        print("✅ FILMARILE S-AU INCHEIAT.")
        context.browser.close()