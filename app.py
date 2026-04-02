import streamlit as st
import pandas as pd
from PIL import Image

import database as db
import pdf_generator as pg

# --- Perusasetukset ---
st.set_page_config(
    page_title="Mega Taloushallinto",
    page_icon="assets/page_icon.png",
    layout="wide"
)

# Luodaan tietokanta tarvittaessa
db.luo_tietokanta()

# --- Tyylimäärittelyt (CSS) ---
st.markdown(
    """
    <style>
    /* Metric-kortit */
    div[data-testid="metric-container"] {
        background-color: #f1f8fa;
        border: 1px solid #c9dbe0;
        padding: 10px 15px;
        border-radius: 8px;
        color: #0a4b61;
    }
    div[data-testid="metric-container"] label {
        font-weight: bold;
    }

    /* Keskitetty kirjautumislaatikko */
    .centered-box {
        max-width: 420px;
        margin: 0 auto;
        padding: 2rem 2.5rem;
        border-radius: 12px;
        border: 1px solid #e0e4ea;
        background-color: #ffffff;
        box-shadow: 0 4px 18px rgba(0,0,0,0.04);
    }

    /* Piilota Streamlitin oletusmenu ja footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session ---
if "user" not in st.session_state:
    st.session_state.user = None

# --- KIRJAUTUMINEN / REKISTERÖITYMINEN ---
if st.session_state.user is None:
    st.markdown(
        "<h1 style='text-align: center; color: #0a4b61;'>🛡️ MEGA "
        "<span style='color: #ff7f0e;'>TALOUSHALLINTO</span></h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; font-style: italic;'>Ammattimainen kumppanisi kevytyrittäjyyteen</p>",
        unsafe_allow_html=True,
    )
    st.write("")
    with st.container():
        with st.columns([1, 2, 1])[1]:
            with st.container():
                st.markdown("<div class='centered-box'>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["Kirjaudu", "Rekisteröidy"])

                with tab1:
                    u = st.text_input("Tunnus")
                    p = st.text_input("Salasana", type="password")
                    if st.button("Kirjaudu sisään", use_container_width=True):
                        res = db.kirjaudu(u, p)
                        if res:
                            st.session_state.user = {
                                "id": res[0],
                                "nimi": res[1],
                                "vero": res[2],
                            }
                            st.rerun()
                        else:
                            st.error("Virheelliset tunnukset.")

                with tab2:
                    rt = st.text_input("Uusi tunnus")
                    rs = st.text_input("Uusi salasana", type="password")
                    rn = st.text_input("Nimesi")
                    rv = st.number_input("Veroprosentti", value=15.0, min_value=0.0, max_value=60.0)
                    if st.button("Luo Mega-tili", use_container_width=True):
                        if db.rekisteroi(rt, rs, rn, rv):
                            st.success("Tili luotu! Voit nyt kirjautua sisään.")
                        else:
                            st.error("Tunnus on jo käytössä tai tapahtui virhe.")
                st.markdown("</div>", unsafe_allow_html=True)

# --- PÄÄNÄKYMÄ ---
else:
    # --- SIVUPALKKI ---
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
                <div style="font-size:1.8rem;">🛡️</div>
                <div>
                    <div style="font-weight:700; font-size:1.05rem;">MEGA Taloushallinto</div>
                    <div style="font-size:0.85rem; color:#dbe9f0;">Kevytyrittäjän palkkalaskenta</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"**Käyttäjä:** {st.session_state.user['nimi']}")
        st.write("")

        valinta = st.radio(
            "Valikko",
            ["🏠 Laskuri", "📊 Dashboard", "📜 Historia"],
            index=0,
        )

        st.write("")
        if st.button("Kirjaudu ulos", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # --- LASKURI ---
    if valinta.startswith("🏠"):
        st.title("🧮 Palkkalaskuri")

        st.info(
            "💡 Laske laskutussummasta käteen jäävä osuus helposti. "
            "Brändätty Mega Taloushallinto -palvelulle."
        )

        col_input, col_result = st.columns([1.1, 1.2])

        with col_input:
            st.subheader("Laskelman tiedot")
            brutto = st.number_input(
                "Syötä laskutussumma (€)",
                min_value=0.0,
                step=100.0,
                value=0.0,
            )

            oletus_vero = st.session_state.user["vero"]
            if oletus_vero > 10:
                oletus_vero = 6.0

            vero_p = st.slider(
                "Vero %",
                min_value=0.0,
                max_value=10.0,
                value=float(oletus_vero),
                step=0.5,
            )

            # Laskenta
            palvelu = brutto * 0.0395
            vakuutus = brutto * 0.0300
            tyel = brutto * 0.0715
            vero_euro = brutto * (vero_p / 100)
            netto = brutto - palvelu - vakuutus - tyel - vero_euro

            st.write("")
            if st.button("💾 Tallenna Mega-arkistoon", use_container_width=True):
                if brutto > 0:
                    db.tallenna_laskelma(
                        st.session_state.user["id"],
                        brutto,
                        vero_p,
                        palvelu,
                        vakuutus,
                        tyel,
                        vero_euro,
                        netto,
                    )
                    st.success("Laskelma tallennettu Mega-arkistoon.")
                else:
                    st.warning("Syötä ensin laskutussumma ennen tallennusta.")

            with st.expander("Näytä kulujen erittely"):
                st.write(f"Palvelumaksu (3,95%): **{palvelu:.2f} €**")
                st.write(f"Vakuutusturva (3,00%): **{vakuutus:.2f} €**")
                st.write(f"TyEL-maksuarvio (7,15%): **{tyel:.2f} €**")
                st.write(f"Ennakonpidätys ({vero_p:.2f}%): **{vero_euro:.2f} €**")

        with col_result:
            st.subheader("Tulokset")
            c1, c2, c3 = st.columns(3)
            c1.metric("Nettopalkka", f"{netto:.2f} €")
            c2.metric("Bruttopalkka", f"{brutto:.2f} €")
            c3.metric("Verot yhteensä", f"{vero_euro:.2f} €")

            st.write("")
            st.markdown("### Tulokehitys (Netto)")

            hist = db.hae_historia(st.session_state.user["id"])
            if hist:
                df = pd.DataFrame(
                    hist,
                    columns=[
                        "ID",
                        "KayttajaID",
                        "Brutto",
                        "Vero%",
                        "Palvelu",
                        "Vakuutus",
                        "TyEL",
                        "Vero€",
                        "Netto",
                        "Pvm",
                    ],
                )
                df_plot = df.set_index("Pvm")["Netto"].sort_index()
                st.bar_chart(df_plot, color="#0a4b61")
            else:
                st.caption("Tallennetut laskelmat näkyvät tässä graafina.")

    # --- DASHBOARD ---
    elif valinta.startswith("📊"):
        st.title("📊 Tulojen analyysi")

        hist = db.hae_historia(st.session_state.user["id"])
        if hist:
            df = pd.DataFrame(
                hist,
                columns=[
                    "ID",
                    "KayttajaID",
                    "Brutto",
                    "Vero%",
                    "Palvelu",
                    "Vakuutus",
                    "TyEL",
                    "Vero€",
                    "Netto",
                    "Pvm",
                ],
            )

            c1, c2, c3 = st.columns(3)
            c1.metric("Kokonaislaskutus", f"{df['Brutto'].sum():.2f} €")
            if len(df) > 1:
                delta = df["Netto"].iloc[-1] - df["Netto"].iloc[0]
            else:
                delta = df["Netto"].iloc[0]
            c2.metric("Netto yhteensä", f"{df['Netto'].sum():.2f} €", delta=f"{delta:.2f} €")
            c3.metric("Maksetut verot", f"{df['Vero€'].sum():.2f} €")

            st.write("")
            st.markdown("### Tulokehitys per kuukausi (Netto)")

            df_plot = df.set_index("Pvm")["Netto"].sort_index()
            st.bar_chart(df_plot, color="#0a4b61")

            st.write("")
            st.markdown("### Viimeisimmät laskelmat")
            st.dataframe(
                df[["Pvm", "Brutto", "Netto", "Vero€"]],
                use_container_width=True,
            )
        else:
            st.info("Tallenna ensimmäinen laskelmasi, niin näet analyysin täällä.")

    # --- HISTORIA ---
    elif valinta.startswith("📜"):
        st.title("📜 Laskuhistoria")

        hist = db.hae_historia(st.session_state.user["id"])
        if not hist:
            st.info("Ei vielä tallennettuja laskelmia.")
        else:
            for h in hist:
                otsikko = f"{h[9]} — Netto: {h[8]:.2f} €"
                with st.expander(otsikko):
                    st.write(f"**Bruttopalkka:** {h[2]:.2f} €")
                    st.write(f"**Vero %:** {h[3]:.2f} %")
                    st.write(f"**Palvelumaksu:** {h[4]:.2f} €")
                    st.write(f"**Vakuutusturva:** {h[5]:.2f} €")
                    st.write(f"**TyEL:** {h[6]:.2f} €")
                    st.write(f"**Verot yhteensä:** {h[7]:.2f} €")
                    st.write(f"**Netto:** {h[8]:.2f} €")
                    st.write(f"**Päivämäärä:** {h[9]}")

                    pdf = pg.luo_palkkakuitti_pdf(st.session_state.user["nimi"], h)
                    st.download_button(
                        "Lataa palkkakuitti PDF-muodossa",
                        pdf,
                        file_name=f"mega_{h[0]}.pdf",
                        mime="application/pdf",
                    )