from fpdf import FPDF

def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)  # Обычный
    pdf.add_font('DejaVu', 'B', 'fonts/DejaVuSans-Bold.ttf', uni=True)  # Жирный

    pdf.set_font("DejaVu", "B", size=16)
    pdf.cell(200, 10, txt="Звіт про посіви", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("DejaVu", "", size=12)
    for record in data:
        line = f"Культура: {record['culture']}, Площа: {record['area']} га, Дата посіву: {record['sowing_date']}, Прогноз дозрівання: {record['maturation_days']} днів"
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output("report.pdf", 'F')
