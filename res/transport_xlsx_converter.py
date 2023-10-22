# Import the pdfplumber library for PDF extraction and the pandas library for data manipulation
import pdfplumber
import pandas as pd

# Specify the path to the input PDF file
pdf_file = "res/files/transport.pdf"

# Specify the path for the output Excel file
output_excel = "res/files/transport.xlsx"

# Open the PDF file using pdfplumber
with pdfplumber.open(pdf_file) as pdf:
    # Access the first page of the PDF (page index 0)
    page = pdf.pages[0]
    
    # Extract tabular data from the page (if present)
    table = page.extract_table()
    
    if table:
        # If tabular data is successfully extracted, create a pandas DataFrame
        df = pd.DataFrame(table)
        
        # Write the DataFrame to an Excel file without including the index
        df.to_excel(output_excel, index=False, sheet_name="Sheet1")
        
        # Print a message indicating the successful extraction and saving of the table
        print(f"Table extracted and saved as {output_excel}")
