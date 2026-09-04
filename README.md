# VitalsDemo

Kevyt Flask-pohjainen potilasvalvonnan harjoitussovellus. Käytetään
**Potilasvalvonnan laitteet** -kurssin (TX00EY15, Metropolia AMK) Tuntitehtävä
4:n aamupäivässä Robot Framework -testiautomaation harjoitteluun.

> ⚠️ Tämä on **opetustarkoitukseen tehty harjoitusympäristö**, ei
> tuotantotasoinen sovellus. Se ei täytä HIPAA/GDPR-vaatimuksia eikä sisällä
> oikeaa potilasdataa — kaikki nimet ja mittausarvot ovat kuvitteellisia.

## Asennus ja käynnistys

```bash
pip install -r requirements.txt
python init_db.py
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
