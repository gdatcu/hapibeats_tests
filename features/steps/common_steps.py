# Fisier: features/steps/common_steps.py
from behave import *

@given('Sunt autentificat in aplicatie')
def step_impl(context):
    """
    Acest pas este o preconditie reutilizabila.
    Efectueaza un login complet si verifica succesul
    inainte ca scenariul propriu-zis sa continue.
    """
    context.login_page.load()
    context.login_page.introdu_username("george.datcu")
    context.login_page.introdu_parola("qazXSW13")
    context.login_page.apas_buton_login()
    context.login_page.verifica_login_reusit("You Might Also Like")
