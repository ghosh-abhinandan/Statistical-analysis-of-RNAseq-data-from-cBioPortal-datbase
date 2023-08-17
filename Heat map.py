import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Replace this with the actual path to your gene expression data Excel file (.xlsx)
data_path = 'D:\In silico\Jeremy Ovarian\JEREMY OVARIAN\Modified\Modified\Normalized_Files\'

# Load the gene expression data from Excel
df = pd.read_excel(data_path, index_col=0)  # Assuming the first column is the gene names and used as index

# Create a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df, cmap='viridis', annot=False, fmt=".2f", linewidths=0.5)
plt.title('Gene Expression Heatmap')
plt.xlabel('Samples')
plt.ylabel('Genes')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the heatmap
plt.show()
