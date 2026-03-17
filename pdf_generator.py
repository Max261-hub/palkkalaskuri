from fpdf import FPDF

def luo_palkkakuitti_pdf(kayttaja_nimi, d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 15, "VIRALLINEN PALKKALASKELMA", ln=True, align="C")
    
    pdf.set_font("helvetica", "", 12)
    pdf.ln(10)
    pdf.cell(0, 8, f"Saaja: {kayttaja_nimi}", ln=True)
    pdf.cell(0, 8, f"Paivamaara: {d[9]}", ln=True)
    pdf.line(10, 50, 200, 50)
    pdf.ln(10)
    
    # Eritellyt rivit
    pdf.cell(100, 8, f"Laskutettu brutto (ALV 0%):")
    pdf.cell(0, 8, f"{d[2]:.2f} EUR", align="R", ln=True)
    pdf.cell(100, 8, f"Palvelumaksu (3.95%):")
    pdf.cell(0, 8, f"-{d[4]:.2f} EUR", align="R", ln=True)
    pdf.cell(100, 8, f"Vakuutusturva (3.00%):")
    pdf.cell(0, 8, f"-{d[5]:.2f} EUR", align="R", ln=True)
    pdf.cell(100, 8, f"TyEL-maksuarvio:")
    pdf.cell(0, 8, f"-{d[6]:.2f} EUR", align="R", ln=True)
    pdf.cell(100, 8, f"Ennakonpidatys ({d[3]}%):")
    pdf.cell(0, 8, f"-{d[7]:.2f} EUR", align="R", ln=True)
    
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(100, 12, "MAKSETTU NETTOYHTEENSA:")
    pdf.cell(0, 12, f"{d[8]:.2f} EUR", align="R", ln=True)

    # TÄRKEÄ KORJAUS: Muunnos bytes-muotoon, jotta selain hyväksyy latauksen
    return bytes(pdf.output())