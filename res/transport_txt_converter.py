# Import the pandas library, which is commonly used for data manipulation
import pandas as pd

# Define the path to the Excel file containing transport information
excel_file = "res/files/transport.xlsx"

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)

# Define a function to format data from each row into a sentence
def format_data_to_sentence(row):
    # Create a sentence using the values from the DataFrame
    sentence = f"Bus number {row['Bus Number']} goes on the line {row['Ligne']}. The departure locations for this bus are {row['Vendredi']} on Friday, {row['Samedi']} on Saturday, and {row['Dimanche']} on Sunday. The schedules for some days in the week are: {row['Horaires']}."
    
    return sentence

# Define the path for the output text file
output_file = "res/files/transport.txt"

# Open the output text file for writing with UTF-8 encoding
with open(output_file, "w", encoding="utf-8") as file:
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Format the data into a sentence
        sentence = format_data_to_sentence(row)
        # Write the sentence to the text file with an empty line as a separator
        file.write(sentence + "\n\n")

# Print a message indicating the successful creation of the text file
print(f"Text file '{output_file}' created successfully.")
