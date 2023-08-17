import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# Set the directory paths
input_dir = "D:\In silico\Jeremy Ovarian\JEREMY OVARIAN\Modified\Modified"
output_dir = "C:/Users/KIIT/Desktop/Plots"

# Get the list of Excel files in the input directory
excel_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith(".xlsx")]

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each Excel file
for file_path in excel_files:
    # Extract the file name without extension
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Read the Excel file
    data = pd.read_excel(file_path)

    # Identify the column name for the grade
    grade_column = "Neoplasm Histologic Grade"

    # Identify the value column dynamically based on its content
    value_column = [col for col in data.columns if re.search("mRNA expression \(RNA Seq V2 RSEM\)", col)]

    # Check if the value column exists
    if not value_column:
        print("Value column not found in file:", file_path)
        continue  # Skip to the next file

    # Extract the gene name from the value column using regular expressions
    gene_name = re.search(r"^[^:]+", value_column[0]).group()

    # Filter the data for G1, G2, G3, and High Grade groups
    groups = data[data[grade_column].isin(["G1", "G2", "G3", "G4"])]

    # Create the box plot
    plt.figure()
    groups.boxplot(column=value_column[0], by=grade_column, grid=False, patch_artist=True, meanline=True)
    plt.xlabel("Cancer")
    plt.ylabel("mRNA expression level")
    plt.title(file_name)
    plt.suptitle("")  # Remove default sub-title
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PNG file in the output directory
    output_path = os.path.join(output_dir, f"{file_name}.png")
    plt.savefig(output_path, dpi=300)
    plt.close()

print("Box plots generated successfully.")
