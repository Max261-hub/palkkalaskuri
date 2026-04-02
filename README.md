# 🛡️ MEGA Taloushallinto  
Kevytyrittäjän palkkalaskuri & tulojen seurantatyökalu

Tämä sovellus on toteutettu osana ohjelmistokehityksen näyttöä.  
Sovellus on suunniteltu kevytyrittäjille helpottamaan laskutuksen, verojen ja nettopalkan laskemista sekä tulojen seurantaa.

---

## Projektin tavoitteet

- Rakentaa **toimiva ja turvallinen kirjautumisjärjestelmä**
- Toteuttaa **palkkalaskuri**, joka huomioi:
  - palvelumaksun (3,95 %)
  - vakuutusturvan (3,00 %)
  - TyEL-maksuarvion (7,15 %)
  - käyttäjän oman veroprosentin
- Tallentaa laskelmat **SQLite-tietokantaan**
- Näyttää tulot **dashboard-kaaviona**
- Mahdollistaa **PDF-palkkakuitin lataamisen**
- Toteuttaa **brändätty käyttöliittymä** (MEGA Taloushallinto)

---

## Teknologiat

| Osa | Teknologia |
|-----|------------|
| Käyttöliittymä | Streamlit |
| Tietokanta | SQLite3 |
| PDF-luonti | FPDF2 |
| Kieli | Python |
| Tyylit | CSS + Streamlit Theme |

---

## 📂 Projektin rakenne
|assets
|    /page_icon.png
|streamlit
|     /config.toml
|app.py
|database.py
|mega_talous.db
|pdf_generator.py
|README.md
|requirments.txt


---

## Käyttäjähallinta

- Käyttäjä voi **rekisteröityä** ja **kirjautua sisään**
- Salasana tallennetaan **SHA-256 hashina**
- Jokaisella käyttäjällä on oma veroprosentti ja oma laskuhistoria

---

## 🧮 Palkkalaskuri

Laskuri laskee automaattisesti:

- palvelumaksu = 3,95 %
- vakuutusturva = 3,00 %
- TyEL = 7,15 %
- verot = käyttäjän valitsema %

Lopputuloksena näytetään:

- **nettopalkka**
- **bruttopalkka**
- **verot yhteensä**
- **kulujen erittely**

---

## 📊 Dashboard

Dashboard näyttää:

- kokonaislaskutuksen
- maksetut verot
- nettopalkan kehityksen
- kaavion tuloista
- taulukon viimeisimmistä laskelmista

---

## 📜 Historia

Historia-sivulla käyttäjä voi:

- tarkastella kaikkia laskelmiaan
- ladata **PDF-palkkakuitin**

---

## 📄 PDF-palkkakuitti

PDF sisältää:

- käyttäjän nimen
- päivämäärän
- bruttopalkan
- kaikki kulut eriteltynä
- nettopalkan

PDF luodaan FPDF2-kirjastolla.

---

## Asennus
1. Kloonaa repositorio
2. Asenna riippuvuudet: `pip install -r requirements.txt`
3. Käynnistä sovellus: `streamlit run app.py`


## Oppimispäiväkirja (Virheenkorjaus)
Kehityksen aikana havaittiin kriittinen virhe PDF-tiedoston latauksessa (`StreamlitAPIException`). 
Ongelma ratkaistiin muuntamalla `bytearray`-tyyppinen data standardiin `bytes`-muotoon, 
mikä varmisti tiedoston eheyden latausvaiheessa.

                +----------------------+
                |      Käyttäjä        |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |      Streamlit       |
                |      app.py          |
                +----------+-----------+
                           |
        +------------------+------------------+
        |                                     |
        v                                     v
+---------------+                     +----------------+
| database.py   |                     | pdf_generator.py|
| SQLite3       |                     | FPDF2           |
+-------+-------+                     +--------+--------+
        |                                       |
        v                                       v
+---------------+                     +----------------+
| kayttajat     |                     | PDF palkkakuitti|
| palkat        |                     +----------------+
+---------------+