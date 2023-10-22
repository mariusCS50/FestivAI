import pdfplumber
import pandas as pd

pdf_file = "transport.pdf"
output_excel = "transport.xlsx"

with pdfplumber.open(pdf_file) as pdf:
    page = pdf.pages[0]
    table = page.extract_table()
    if table:
        df = pd.DataFrame(table)
        df.to_excel(output_excel, index=False, sheet_name="Sheet1")
        print(f"Table extracted and saved as {output_excel}")