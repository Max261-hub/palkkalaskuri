import streamlit as st          # Käyttöliittymäkirjasto
import database as db
import pdf_generator as pg
import pandas as pd

# Sovelluksen asetukset
st.set_page_config(page_title="Palkka.fi - Kevytyrittäjä", layout="wide", page_icon="💼")
db.luo_tietokanta()

# SESSION STATE (Istunnon hallinta)
# Tämä muistaa kuka on kirjautunut sisään, vaikka sivu latautuisi uudelleen.
if "user" not in st.session_state:
    st.session_state.user = None

# --- SISÄÄNKIRJAUDU ---
# EHTOLAUSE (if-else): Hallitsee mitä käyttäjä näkee
if st.session_state.user is None:
    st.title("Kevytyrittäjä-portaali")
    t1, t2 = st.tabs(["Kirjaudu", "Rekisteröidy"])
    with t1:
        u = st.text_input("Käyttäjätunnus")
        p = st.text_input("Salasana", type="password")
        if st.button("Kirjaudu"):
            res = db.kirjaudu(u, p)
            if res:
                st.session_state.user = {"id": res[0], "nimi": res[1], "vero": res[2]}
                st.rerun()
            else: st.error("Väärä tunnus tai salasana.")
    with t2:
        rt, rs = st.text_input("Valitse tunnus"), st.text_input("Valitse salasana", type="password")
        rn, rv = st.text_input("Nimesi"), st.number_input("Veroprosentti", value=15.0)
        if st.button("Luo tili"):
            if db.rekisteroi(rt, rs, rn, rv): st.success("Tili luotu!")

# --- PÄÄVALIKKO ---
else:
    with st.sidebar:
        st.header(f"Tervetuloa, {st.session_state.user['nimi']}")
        valinta = st.radio("Valitse toiminto", ["Laskuri", "📊 Dashboard", "📜 Historia"])
        if st.button("Kirjaudu ulos"):
            st.session_state.user = None
            st.rerun()

    # --- LASKURI ---
    if valinta == "Laskuri":
        st.title("🧮 Palkkalaskuri")
        st.info("💡 Laske laskutussummasta käteen jäävä osuus helposti.")
        
        mode = st.radio("Laskentatapa", ["Laske brutosta netto", "Laske netosta brutto (Tavoite)"])
        
        if mode == "Laske brutosta netto":
            brutto = st.number_input("Syötä laskutussumma (€)", min_value=0.0, step=100.0)
            vero_p = st.slider("Vero %", 0.0, 60.0, st.session_state.user['vero'])
            
            # Laskenta kertoimilla
            p_maksu, v_maksu = brutto * 0.0395, brutto * 0.0300
            tyel, v_euro = brutto * 0.0715, brutto * (vero_p / 100)
            netto = brutto - p_maksu - v_maksu - tyel - v_euro
            
            if brutto > 0:
                st.success(f"Nettopalkka: {netto:.2f} €")
                if st.button("💾 Tallenna arkistoon"):
                    db.tallenna_laskelma(st.session_state.user['id'], brutto, vero_p, p_maksu, v_maksu, tyel, v_euro, netto)
                    st.toast("Tallennettu!")

        else: # Tavoitetulon laskenta
            tavoite = st.number_input("Kuinka paljon haluat käteen (netto, €)?", min_value=0.0)
            vero_p = st.session_state.user['vero']
            # Käänteinen laskentakaava (yksinkertaistettu)
            tarvittava_brutto = tavoite / (1 - 0.0395 - 0.0300 - 0.0715 - (vero_p/100))
            if tavoite > 0:
                st.warning(f"Sinun tulee laskuttaa vähintään: {tarvittava_brutto:.2f} €")

    # --- DASHBOARD ---
    elif valinta == "📊 Dashboard":
        st.title("📊 Tulojen seuranta")
        data = db.hae_historia(st.session_state.user['id'])
        if data:
            df = pd.DataFrame(data, columns=['ID','UID','Brutto','VeroP','PM','VM','TyEL','VEuro','Netto','Pvm'])
            df['Pvm'] = pd.to_datetime(df['Pvm'], dayfirst=True)
            
            c1, c2 = st.columns(2)
            c1.metric("Kokonaistulot (Brutto)", f"{df['Brutto'].sum():.2f} €")
            c2.metric("Yhteensä käteen (Netto)", f"{df['Netto'].sum():.2f} €")
            
            st.subheader("Tulokehitys (Netto)")
            st.line_chart(df.set_index('Pvm')['Netto'])
        else: st.info("Ei vielä tallennettuja tietoja.")

    # --- HISTORIA ---
    elif valinta == "📜 Historia":
        st.title("📜 Kuittihistoria")
        hist = db.hae_historia(st.session_state.user['id'])
        for h in hist:
            with st.expander(f"📅 {h[9]} | Netto: {h[8]:.2f} €"):
                pdf_data = pg.luo_palkkakuitti_pdf(st.session_state.user['nimi'], h)
                st.download_button("📥 Lataa PDF-kuitti", data=pdf_data, file_name=f"kuitti_{h[0]}.pdf", mime="application/pdf", key=f"d_{h[0]}")