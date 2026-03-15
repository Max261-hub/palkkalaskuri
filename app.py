import streamlit as st
import database as db
import pdf_generator as pg

st.set_page_config(page_title="Kevytyrittäjä Portal", layout="centered")
db.luo_tietokanta()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("💼 Kirjaudu sisään")
    t1, t2 = st.tabs(["Kirjaudu", "Rekisteröidy"])
    with t1:
        u = st.text_input("Tunnus")
        p = st.text_input("Salasana", type="password")
        if st.button("Kirjaudu"):
            user = db.kirjaudu(u, p)
            if user:
                st.session_state.user = {"id": user[0], "nimi": user[1], "vero": user[2]}
                st.rerun()
            else: st.error("Väärät tunnukset")
    with t2:
        rt = st.text_input("Uusi tunnus")
        rs = st.text_input("Uusi salasana", type="password")
        rn = st.text_input("Nimesi")
        rv = st.number_input("Vero %", value=15.0)
        if st.button("Luo tili"):
            if db.rekisteroi(rt, rs, rn, rv): st.success("Tili luotu!")
else:
    st.sidebar.write(f"Hei, {st.session_state.user['nimi']}")
    sivu = st.sidebar.radio("Navigointi", ["Laskuri", "Historia"])
    if st.sidebar.button("Kirjaudu ulos"):
        st.session_state.user = None
        st.rerun()

    if sivu == "Laskuri":
        st.title("🧮 Palkkalaskuri")
        st.markdown("Palkkalaskurilla lasket kätevästi paljonko asiakkaalta laskutettavasta summasta jää sinulle käteen.")
        st.info("💡 Laske laskutussummasta käteen jäävä osuus helposti.")
        
        brutto = st.number_input("Laskutussumma (€)", min_value=0.0, step=100.0)
        vero_p = st.slider("Vero %", 0.0, 60.0, st.session_state.user['vero'])
        
        p_maksu = brutto * 0.0395
        v_maksu = brutto * 0.0300
        tyel = brutto * 0.0715
        v_euro = brutto * (vero_p / 100)
        netto = brutto - p_maksu - v_maksu - tyel - v_euro
        
        if brutto > 0:
            st.write(f"Nettopalkka: **{netto:.2f} €**")
            if st.button("💾 Tallenna"):
                db.tallenna_laskelma(st.session_state.user['id'], brutto, vero_p, p_maksu, v_maksu, tyel, v_euro, netto)
                st.toast("Tallennettu!")

    elif sivu == "Historia":
        st.title("📜 Historia")
        hist = db.hae_historia(st.session_state.user['id'])
        for h in hist:
            with st.expander(f"Päiväys: {h[9]} | Netto: {h[8]:.2f} €"):
                pdf_bytes = pg.luo_palkkakuitti_pdf(st.session_state.user['nimi'], h)
                st.download_button("📥 Lataa PDF", data=pdf_bytes, file_name=f"kuitti_{h[0]}.pdf", mime="application/pdf", key=f"btn_{h[0]}")