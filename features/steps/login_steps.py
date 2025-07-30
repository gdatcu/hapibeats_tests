# Fisier: features/steps/login_steps.py
from behave import *
use_step_matcher("parse")

@given('Sunt pe pagina de login a HapiBeats')
def step_impl(context): context.login_page.load()

@when('Introduc username-ul "{u}" si parola "{p}"')
def step_impl(context, u, p):
    context.login_page.introdu_username(u)
    context.login_page.introdu_parola(p)

@when('Apas pe butonul de login')
def step_impl(context): context.login_page.apas_buton_login()

@then('Ar trebui sa fiu autentificat si sa vad pagina principala')
def step_impl(context): context.login_page.verifica_login_reusit("You Might Also Like")

@then('Ar trebui sa vad un mesaj de eroare pentru login esuat')
def step_impl(context): context.login_page.verifica_mesaj_eroare("Your username or password was incorrect")

# new comment