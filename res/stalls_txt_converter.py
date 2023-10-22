import pandas as pd

excel_file = "res/stalls.xlsx"

df = pd.read_excel(excel_file)

def format_data_to_sentence(row):
    sentence = f"At '{row['stall_name']}' you can have the following drink categories: {row['drink_categories']}, and the following food types: {row['food_types']}. The place number of this stall is {row['place_number']} and it's booking weezpay account number is {row['booking_weezpay_account']}"

    return sentence

output_file = "res/stalls.txt"
with open(output_file, "w", encoding="utf-8") as file:
    for index, row in df.iterrows():
        sentence = format_data_to_sentence(row)
        file.write(sentence + "\n\n")

print(f"Text file '{output_file}' created successfully.")
