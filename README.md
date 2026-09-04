# VitalsDemo

Kevyt Flask-pohjainen potilasvalvonnan harjoitussovellus. Käytetään
**Potilasvalvonnan laitteet** -kurssin (TX00EY15, Metropolia AMK) Tuntitehtävä
4:n aamupäivässä Robot Framework -testiautomaation harjoitteluun.

> ⚠️ Tämä on **opetustarkoitukseen tehty harjoitusympäristö**, ei
> tuotantotasoinen sovellus. Se ei täytä GDPR-vaatimuksia eikä sisällä
> oikeaa potilasdataa — kaikki nimet ja mittausarvot ovat kuvitteellisia.
>
> **Tarkoitettu ajettavaksi vain paikallisesti** (`localhost`) opetus- ja
> harjoituskäyttöön. Sovelluksessa ei ole CSRF-suojausta eikä muita
> tuotantotason turvamekanismeja, joten sitä ei pidä julkaista julkiseen
> verkkoon tai muuhun kuin omaan, paikalliseen ympäristöön.

## Asennus ja käynnistys

Vaatii Python 3.10 tai uudemman ([python.org/downloads](https://www.python.org/downloads/)).

### 1. Kloonaa repositorio

```bash
git clone https://github.com/sakluk/vitals-demo.git
cd vitals-demo
```

Jos sinulla ei ole Gitiä komentoriviltä, voit myös ladata repon ZIP-tiedostona
GitHubin "Code" → "Download ZIP" -napista ja purkaa se koneellesi.

### 2. Luo ja aktivoi virtuaaliympäristö

Virtuaaliympäristö (`.venv`) pitää tämän projektin Python-paketit erillään
muista projekteista ja järjestelmän Pythonista. Suositellaan, ei pakollinen.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> Jos aktivointi antaa virheen skriptien suorittamisesta, aja ensin
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ja yritä uudelleen.

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Kun ympäristö on aktivoitu, komentorivin alkuun ilmestyy `(.venv)`. Ympäristön
voi sulkea komennolla `deactivate`.

### 3. Asenna riippuvuudet ja alusta tietokanta

```bash
pip install -r requirements.txt
python init_db.py
```

### 4. Käynnistä sovellus

```bash
python app.py
```

Sovellus käynnistyy osoitteeseen **http://localhost:5000**.

## Kirjautumistunnukset

| Käyttäjätunnus | Salasana | Rooli |
|---|---|---|
| `hoitaja` | `hoitaja123` | Hoitaja |
| `laakari` | `laakari123` | Lääkäri |

## Roolit

- **Hoitaja**: selaa potilaita ja mittauksia, lisää mittauksia. Ei voi
  lisätä/poistaa potilaita eikä muokata lääkärin huomioita.
- **Lääkäri**: kaikki hoitajan oikeudet + potilaiden lisäys/poisto, lääkärin
  huomioiden kirjaus, käyttäjätilastojen näkeminen potilaslistalla.

## Rakenne

```
vitals-demo/
├── app.py              # Flask-sovelluksen pääohjelma
├── auth.py             # Kirjautuminen (Flask-Login, bcrypt)
├── routes.py            # URL-reitit ja validointilogiikka
├── models.py             # Tietokantatoiminnot (raw SQLite, ei ORM)
├── init_db.py           # Tietokannan alustus + esimerkkidata
├── requirements.txt
├── templates/            # Jinja2-templatet (Bootstrap 5)
├── static/               # custom.css
└── tests/                 # Robot Framework -testit (ks. tests/README.md)
```

## Testit

Katso [tests/README.md](tests/README.md) Robot Framework -ympäristön
asennus- ja ajo-ohjeet.

## Tausta

Sovellus on toteutettu Claude Codella vaatimusmäärittelyn
`VitalsDemo_vaatimusmaarittely.md` mukaisesti (kurssirepositorion
`private/`-kansio).
