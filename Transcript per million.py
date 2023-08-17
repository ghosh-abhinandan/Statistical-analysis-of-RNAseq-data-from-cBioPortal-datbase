import os
import pandas as pd
from openpyxl import Workbook

# Set the folder path
folder_path ="D:\In silico\Jeremy Ovarian\JEREMY OVARIAN\Modified"

# List all files in the folder
file_list = [f for f in os.listdir(folder_path) if f.endswith(".xlsx")]

# Set the export directory for TPM-normalized files
export_folder ="D:\In silico\Jeremy Ovarian\JEREMY OVARIAN\Modified\TPM"
os.makedirs(export_folder, exist_ok=True)


# Function for TPM normalization
def tpm_normalize(x):
    if isinstance(x, (int, float)):
        return x / (sum(x) / 1e6)  # Normalize to one million reads
    else:
        return x


# Loop through each file, perform TPM normalization, and save the new file
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)

    # Read the data from the first sheet
    data = pd.read_excel(file_path, sheet_name=0)

    # Apply TPM normalization to each column in the dataset
    normalized_data = data.apply(tpm_normalize, axis=0)

    # Create a new workbook
    wb = Workbook()

    # Create a new sheet with the normalized data
    sheet = wb.active
    sheet.title = "TPM_Normalized_Data"
    for r_idx, row in normalized_data.iterrows():
        sheet.append(row.tolist())

    # Save the TPM normalized data as a new Excel file in the export folder
    new_file_name = file_name.replace("_TPM_Normalized.xlsx", ".xlsx")
    new_file_path = os.path.join(export_folder, new_file_name)
    wb.save(new_file_path)

    print("TPM normalization performed on the file:", file_name)

print("TPM normalization and saving completed for all files.")
