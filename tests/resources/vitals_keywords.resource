*** Settings ***
Documentation    Yhteiset avainsanat VitalsDemo-sovelluksen RF-testeille.
Library          Browser

*** Variables ***
${BASE_URL}    http://localhost:5000
${BROWSER}     chromium
${HEADLESS}    False

*** Keywords ***
Open VitalsDemo
    New Browser    ${BROWSER}    headless=${HEADLESS}
    New Page       ${BASE_URL}

Login As
    [Arguments]    ${username}    ${password}
    Go To          ${BASE_URL}/login
    Fill Text      id=username    ${username}
    Fill Text      id=password    ${password}
    Click          id=login-btn

Login As Hoitaja
    Login As    hoitaja    hoitaja123

Login As Laakari
    Login As    laakari    laakari123

Logout
    Click    id=logout-link

Close VitalsDemo
    Close Browser
