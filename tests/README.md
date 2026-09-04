# RF-testiympäristön asennus

Nämä testit on tehty **Tuntitehtävä 4** -harjoitusta varten (Potilasvalvonnan
laitteet, TX00EY15). Testataan VitalsDemo-sovellusta Robot Frameworkin
[Browser-kirjastolla](https://robotframework-browser.org/) (Playwright-pohjainen).

## 1. Asenna riippuvuudet

```bash
pip install robotframework robotframework-browser
rfbrowser init
```

`rfbrowser init` lataa Playwrightin tarvitsemat selainbinäärit (Chromium ym.).
Tämä tehdään vain kerran per kone.

## 2. Käynnistä VitalsDemo

Toisessa terminaalissa, projektin juuresta:

```bash
pip install -r requirements.txt
python init_db.py
python app.py
```

Sovellus käynnistyy osoitteeseen `http://localhost:5000`.

## 3. Aja testit

Projektin `tests/`-kansiosta:

```bash
robot 01_login_tests.robot
robot 02_patient_tests.robot
```

Molemmat kerralla:

```bash
robot .
```

Tulokset (`log.html`, `report.html`) syntyvät ajokansioon.

## 4. Rakenne

| Tiedosto | Tila | Kuvaus |
|---|---|---|
| `resources/vitals_keywords.resource` | Valmis | Yhteiset avainsanat: kirjautuminen, uloskirjautuminen, selaimen avaus |
| `01_login_tests.robot` | Valmis | Esimerkkitestit kirjautumisesta — tutustu tähän ensin |
| `02_patient_tests.robot` | Osittain täytetty | Täydennä `# TODO`-kohdat |

## 5. Elementtien id-tunnisteiden löytäminen

Kaikki VitalsDemo-sovelluksen interaktiiviset elementit (napit, lomakekentät,
taulukot) on merkitty yksilöllisillä `id`-attribuuteilla, joita RF-testeissä
käytetään `id=`-lokaattoreina (esim. `id=login-btn`). Sovelluksessa ei ole
erillistä listaa tunnisteista — etsi ne itse selaimen kehittäjätyökaluilla,
samalla tavalla kuin tekisit oikeassa testausprojektissa:

1. Avaa sivu selaimessa (`http://localhost:5000`) ja paina **F12** (tai
   hiiren oikea painike → **Tutki/Inspect**) avataksesi kehittäjätyökalut.
2. Käytä työkalurivin **elementin valinta** -kuvaketta (nuoli-kursori-ikoni,
   Chromessa/Edgessä vasemmassa yläkulmassa) ja klikkaa haluamaasi elementtiä
   sivulla — esim. kirjautumisnappia tai potilastaulukon riviä.
3. Elementin HTML korostuu **Elements/Elementit**-välilehdellä; etsi
   `id="..."`-attribuutti auenneesta koodista.
4. Käytä löytynyttä arvoa RF-testissä muodossa `id=<arvo>`.

Vinkki: `Ctrl+F` (tai `Cmd+F`) Elements-välilehdellä avaa haun, jolla voi
etsiä esim. `id="save-` löytääkseen kaikki tallennusnapit kerralla.

## 6. Vinkkejä

- `headless=False` (oletus resurssitiedostossa) näyttää selainikkunan — hyvä
  debuggaukseen. Aseta `${HEADLESS}    True`, jos haluat ajaa ilman ikkunaa.
- Jos testi jää jumiin kirjautumisen jälkeen, tarkista että `python init_db.py`
  on ajettu ja tietokanta sisältää oletuskäyttäjät.
- Kun kirjoitat `02_patient_tests.robot`-tiedostoon useamman testitapauksen,
  jotka kirjautuvat sisään eri käyttäjänä (esim. ensin hoitajana, sitten
  lääkärinä), saatat törmätä tilanteeseen, jossa `Login As`-avainsana jää
  odottamaan `id=username`-kenttää loputtomiin eikä testi koskaan etene.
  Tämä ei ole sattumaa — mieti, missä tilassa edellisen testitapauksen
  selainistunto oli, kun se päättyi, ja mitä sille pitäisi tehdä ennen
  seuraavaa kirjautumista. Vihje: katso, miten `01_login_tests.robot`
  huolehtii tästä `Test Teardown`-avainsanallaan.
