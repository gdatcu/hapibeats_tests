# Fisier: features/login.feature
@login
Feature: Autentificarea utilizatorilor

  Scenario: Autentificare cu credentiale valide
    Given Sunt pe pagina de login a HapiBeats
    When Introduc username-ul "george.datcu" si parola "qazXSW13"
    And Apas pe butonul de login
    Then Ar trebui sa fiu autentificat si sa vad pagina principala

  Scenario: Autentificare cu credentiale invalide
    Given Sunt pe pagina de login a HapiBeats
    When Introduc username-ul "user.gresit" si parola "parola.gresita"
    And Apas pe butonul de login
    Then Ar trebui sa vad un mesaj de eroare pentru login esuat
