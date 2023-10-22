import pandas as pd

excel_file = "res/transport.xlsx"

df = pd.read_excel(excel_file)

def format_data_to_sentence(row):
    sentence = f"Bus number {row['Bus Number']} goes on the line {row['Ligne']}. The departure locations for this bus are {row['Vendredi']} on Friday, {row['Samedi']} on Saturday, and {row['Dimanche']} on Sunday. The schedules for some days in the week are: {row['Horaires']}."

    return sentence

output_file = "res/transport.txt"
with open(output_file, "w", encoding="utf-8") as file:
    for index, row in df.iterrows():
        sentence = format_data_to_sentence(row)
        file.write(sentence + "\n\n")

print(f"Text file '{output_file}' created successfully.")
