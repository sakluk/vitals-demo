*** Settings ***
Documentation    OSITTAIN TÄYTETTY — opiskelijat täydentävät puuttuvat testitapaukset.
...              Runko ja resurssit on valmiina; täydennä kohdat, joissa lukee "# TODO".
Resource         resources/vitals_keywords.resource
Suite Setup      Open VitalsDemo
Suite Teardown   Close VitalsDemo

*** Test Cases ***
Hoitaja voi lisata SpO2-mittauksen
    [Documentation]    Kirjaudu hoitajana, avaa ensimmäinen potilas ja lisää SpO2-mittaus.
    ...                Varmista lopuksi, että uusi arvo näkyy mittaustaulukossa.
    Login As Hoitaja
    Click    css=#patient-row-1 a
    Click    id=add-measurement-btn
    # TODO: Valitse parametrityyppi (id=param-type) arvoksi "SpO2"
    # TODO: Syötä kelvollinen arvo kenttään id=value (esim. "96")
    # TODO: Klikkaa id=save-measurement-btn
    # TODO: Varmista Get Text-avainsanalla, että id=measurements-table sisältää arvon "96"

Laakari voi lisata uuden potilaan
    [Documentation]    Kirjaudu lääkärinä ja lisää uusi potilas lomakkeen kautta.
    ...                Varmista, että sovellus ohjaa uuden potilaan tietosivulle ja
    ...                että id=patient-name näyttää syötetyn nimen.
    # TODO: Toteuta koko testitapaus (Login As Laakari, siirtyminen id=add-patient-btn kautta,
    # TODO: lomakkeen täyttö id=patient-name / id=patient-dob / id=patient-room,
    # TODO: lähetys id=save-patient-btn, ja lopputuloksen varmistus)
    Log    TODO: toteuta testi    level=WARN

Hoitaja ei voi lisata potilasta
    [Documentation]    Varmista, ettei hoitajalle näytetä "Lisää potilas" -nappia potilaslistassa
    ...                ja että suora navigointi /patients/add-osoitteeseen palauttaa 403-sivun.
    # TODO: Login As Hoitaja
    # TODO: Varmista Get Element Count tai Get Element States -avainsanalla, ettei id=add-patient-btn ole näkyvissä
    # TODO: Navigoi suoraan osoitteeseen ${BASE_URL}/patients/add
    # TODO: Varmista, että sivulla näkyy "403" tai "Ei käyttöoikeutta"
    Log    TODO: toteuta testi    level=WARN

Virheellinen SpO2-arvo hylataan
    [Documentation]    Yritä tallentaa validointirajojen ulkopuolinen SpO2-arvo (esim. "150")
    ...                ja varmista, että id=measurement-error näyttää virheilmoituksen eikä
    ...                mittausta lisätä taulukkoon.
    # TODO: Login As Hoitaja (tai Laakari)
    # TODO: Siirry potilaan mittauksen lisäyssivulle
    # TODO: Valitse param-type = SpO2, syötä value = 150
    # TODO: Klikkaa id=save-measurement-btn
    # TODO: Varmista Get Text-avainsanalla, että id=measurement-error näkyy ja sisältää virheviestin
