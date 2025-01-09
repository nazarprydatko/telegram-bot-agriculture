import openpyxl

def generate_excel(data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Посіви"
    sheet.append(["ID", "Назва культури", "Площа (га)", "Дата посіву"])

    for row in data:
        sheet.append(row)

    file_path = "crops_report.xlsx"
    workbook.save(file_path)
    return file_path
