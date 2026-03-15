from fpdf import FPDF

def luo_palkkakuitti_pdf(kayttaja_nimi, d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "VIRALLINEN PALKKALASKELMA", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, f"Saaja: {kayttaja_nimi}", ln=True)
    pdf.cell(0, 10, f"Paivamaara: {d[9]}", ln=True)
    pdf.line(10, 45, 200, 45)
    pdf.ln(10)
    pdf.cell(100, 10, f"Laskutus (Brutto): {d[2]:.2f} e", ln=True)
    pdf.cell(100, 10, f"Palvelumaksu (3.95%): -{d[4]:.2f} e", ln=True)
    pdf.cell(100, 10, f"Vakuutusturva (3.00%): -{d[5]:.2f} e", ln=True)
    pdf.cell(100, 10, f"Vero ({d[3]}%): -{d[7]:.2f} e", ln=True)
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(100, 15, f"MAKSETTU NETTO: {d[8]:.2f} e", ln=True)
    
    # Korjaus binäärivirheeseen
    return bytes(pdf.output())