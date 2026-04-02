from fpdf import FPDF


def luo_palkkakuitti_pdf(kayttaja_nimi, d):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Otsikko
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 15, "VIRALLINEN PALKKALASKELMA", ln=True, align="C")

    # Perustiedot
    pdf.set_font("helvetica", "", 12)
    pdf.ln(10)
    pdf.cell(0, 8, f"Saaja: {kayttaja_nimi}", ln=True)
    pdf.cell(0, 8, f"Päivämäärä: {d[9]}", ln=True)
    pdf.line(10, 50, 200, 50)
    pdf.ln(10)

    # Erittely
    labels = [
        ("Laskutettu brutto (ALV 0%):", d[2]),
        ("Palvelumaksu (3,95%):", -d[4]),
        ("Vakuutusturva (3,00%):", -d[5]),
        ("TyEL-maksuarvio:", -d[6]),
        (f"Ennakonpidätys ({d[3]}%):", -d[7]),
    ]

    for teksti, arvo in labels:
        pdf.cell(100, 8, teksti)
        pdf.cell(0, 8, f"{arvo:.2f} EUR", align="R", ln=True)

    # Netto
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(100, 12, "MAKSETTU NETTOYHTEENSÄ:")
    pdf.cell(0, 12, f"{d[8]:.2f} EUR", align="R", ln=True)

    return bytes(pdf.output())