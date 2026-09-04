*** Settings ***
Documentation    VALMIS ESIMERKKI — kirjautumistestit. Näytä tämä opiskelijoille mallina
...              ennen kuin he täydentävät 02_patient_tests.robot-tiedostoa.
Resource         resources/vitals_keywords.resource
Suite Setup      Open VitalsDemo
Suite Teardown   Close VitalsDemo
Test Teardown    Run Keyword If Test Passed    Logout Silently

*** Test Cases ***
Onnistunut kirjautuminen hoitajana
    Login As Hoitaja
    Get Text    id=nav-user-info    contains    hoitaja
    Get Url     contains    /patients

Onnistunut kirjautuminen laakarina
    Login As Laakari
    Get Text    id=nav-user-info    contains    laakari
    Get Url     contains    /patients

Kirjautuminen vaaralla salasanalla nayttaa virheviestin
    Go To          ${BASE_URL}/login
    Fill Text      id=username    hoitaja
    Fill Text      id=password    vaarasalasana
    Click          id=login-btn
    Get Text    id=login-error    contains    Väärä käyttäjätunnus tai salasana

Kirjautunut kayttaja ohjataan suoraan potilaslistaan
    Login As Hoitaja
    Go To       ${BASE_URL}/login
    Get Url     contains    /patients

*** Keywords ***
Logout Silently
    ${url}=    Get Url
    IF    'login' not in $url
        Logout
    END
