# Kevytyrittäjän Palkkalaskuri & Arkisto 

Tämä ohjelmisto on kehitetty osana ohjelmistokehityksen osaamisnäyttöä. Sovellus on suunnattu kevytyrittäjille palkanhallinnan helpottamiseksi.

## Ominaisuudet
- **Suojattu kirjautuminen:** Käyttäjätunnukset ja salasanat (SHA-256 suojattu).
- **Dynaaminen laskenta:** Huomioi automaattisesti palvelumaksun (3,95%) ja vakuutusturvan (3,00%).
- **Kuittihistoria:** Tallentaa kaikki laskelmat SQLite-tietokantaan.
- **PDF-vienti:** Luo virallisen palkkalaskelman ladattavassa PDF-muodossa.

## jätkökehitykset
- Dynaaminen Dashboard: Automaattinen graafinen seuranta tallennetuista tuloista.

- Liiketoiminta-äly: Sovellus sisältää YEL-vakuutusrajan seurannan ja varoittaa käyttäjää velvoitteista.

- Data-analyysi: Hyödynnetään pandas-kirjastoa datan muokkaamiseen ja st.bar_chart-työkalua visualisointiin.

## Tekniset ratkaisut
- **Kieli:** Python
- **Käyttöliittymä:** Streamlit
- **Tietokanta:** SQLite3
- **PDF-kirjasto:** FPDF2
- **Modulaarisuus:** Koodi on jaettu loogisiin moduuleihin (UI, Tietokanta, PDF-generointi).

## Asennus
1. Kloonaa repositorio
2. Asenna riippuvuudet: `pip install -r requirements.txt`
3. Käynnistä sovellus: `streamlit run app.py`


## Oppimispäiväkirja (Virheenkorjaus)
Kehityksen aikana havaittiin kriittinen virhe PDF-tiedoston latauksessa (`StreamlitAPIException`). 
Ongelma ratkaistiin muuntamalla `bytearray`-tyyppinen data standardiin `bytes`-muotoon, 
mikä varmisti tiedoston eheyden latausvaiheessa.
