import os
import pandas as pd

# Set the folder path
folder_path = "D:/In silico/Jeremy Ovarian/JEREMY OVARIAN/Modified/Modified"

# List all files in the folder
file_list = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# Create a new directory to save normalized files
new_folder = os.path.join(folder_path, "Normalized_Files")
os.makedirs(new_folder, exist_ok=True)


# Function for maximum-minimum normalization for each value
def normalize_column(column):
    if column.dtype in (int, float):
        return (column - column.min()) / (column.max() - column.min())
    else:
        return column


# Loop through each file, perform normalization, and save the new file
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)

    # Read the data from the first sheet
    data = pd.read_excel(file_path, sheet_name=0)

    # Apply the normalization to each column in the dataset
    normalized_data = data.apply(normalize_column, axis=0)

    # Create a new Excel writer
    new_file_name = file_name.replace("_Normalized.xlsx", ".xlsx")
    new_file_path = os.path.join(new_folder, new_file_name)
    writer = pd.ExcelWriter(new_file_path, engine='xlsxwriter')

    # Write the normalized data to a new sheet
    normalized_data.to_excel(writer, sheet_name='Normalized_Data', index=False)

    # Save the Excel file
    writer._save()

    print(f"Maximum-minimum normalization performed on each value for the file: {file_name}")

print("Normalization and saving completed for all files.")
