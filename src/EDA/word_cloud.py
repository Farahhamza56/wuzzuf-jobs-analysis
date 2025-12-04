import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load cleaned data
df = pd.read_csv("../../data/cleaned/openfoodfacts_cleaned.csv")

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