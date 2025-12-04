import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("../../data/cleaned/openfoodfacts_cleaned.csv")

#bar chart for most country has products

# Count number of products per country

country_counts = df['countries'].value_counts().head(20)  # Top 20 countries

# Create a bar chart

plt.figure(figsize=(12,6))
plt.bar(country_counts.index, country_counts.values, color='skyblue')
plt.xticks(rotation=45, ha='right')
plt.title('Number of Products per Country (Top 20)')
plt.xlabel('Country')
plt.ylabel('Number of Products')
plt.tight_layout()
plt.show()
#its clear that france has the most products