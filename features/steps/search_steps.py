# Fisier: features/steps/search_steps.py
from behave import *
use_step_matcher("parse")

# Acest pas este acum definit in common_steps.py si va fi gasit automat de behave
# @given('Sunt autentificat in aplicatie')

@when('Navighez la pagina de cautare')
def step_impl(context): context.search_page.navigheaza_la_cautare()

@when('Caut dupa termenul "{termen}"')
def step_impl(context, termen): context.search_page.introdu_termen_cautare(termen)

@then('Ar trebui sa vad o lista de melodii gasite')
def step_impl(context): context.search_page.verifica_existenta_rezultatelor()

@when('Caut dupa un termen care nu exista')
def step_impl(context):
    context.termen_inexistent = "qwertzuiopasdfghjkl"
    context.search_page.introdu_termen_cautare(context.termen_inexistent)

@then('Ar trebui sa vad un mesaj de "No results"')
def step_impl(context): context.search_page.verifica_mesaj_fara_rezultate(context.termen_inexistent)
