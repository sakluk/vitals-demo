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

## 5. Vinkkejä

- Käytä `id=`-lokaattoreita — kaikki interaktiiviset elementit on merkitty
  yksilöllisillä `id`-attribuuteilla (ks. vaatimusmäärittely, kohta 5).
- `headless=False` (oletus resurssitiedostossa) näyttää selainikkunan — hyvä
  debuggaukseen. Aseta `${HEADLESS}    True`, jos haluat ajaa ilman ikkunaa.
- Jos testi jää jumiin kirjautumisen jälkeen, tarkista että `python init_db.py`
  on ajettu ja tietokanta sisältää oletuskäyttäjät.
