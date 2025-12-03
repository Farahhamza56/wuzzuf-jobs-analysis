import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load cleaned data
df = pd.read_csv("data/cleaned/openfoodfacts_cleaned.csv")

# print("\nColumns in dataset:")
# print(df.columns)
# #print(df.head(20))
text = " ".join(str(name) for name in df['product_name'].dropna())
wordcloud = WordCloud(width = 900, height = 900).generate(text)
# Display the generated image:
plt.figure(figsize = (8, 8)) 
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

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

