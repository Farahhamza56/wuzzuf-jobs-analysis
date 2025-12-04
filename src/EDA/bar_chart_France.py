import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("../../data/cleaned/openfoodfacts_cleaned.csv")
#bar chart for most product in france

# Filter data for France

df_france = df[df['countries'].str.contains('France', case=False, na=False)]

# Count top 20 products

top_products = df_france['product_name'].value_counts().head(20)

plt.figure(figsize=(12,6))
plt.bar(top_products.index, top_products.values, color='salmon')
plt.xticks(rotation=90, ha='right')
plt.title('Top 20 Products in France')
plt.xlabel('Product Name')
plt.ylabel('Number of Occurrences')
plt.tight_layout()
plt.show()