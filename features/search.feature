# Fisier: features/search.feature
@search
Feature: Cautarea de continut pe HapiBeats

  Scenario: Cautare cu rezultate
    Given Sunt autentificat in aplicatie
    When Navighez la pagina de cautare
    And Caut dupa termenul "Happy"
    Then Ar trebui sa vad o lista de melodii gasite

  Scenario: Cautare fara rezultate
    Given Sunt autentificat in aplicatie
    When Navighez la pagina de cautare
    And Caut dupa un termen care nu exista
    Then Ar trebui sa vad un mesaj de "No results"