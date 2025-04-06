import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Ensure the "models" directory exists
os.makedirs("models", exist_ok=True)

# Load preprocessed product data
product_df = pd.read_csv("data/cleaned_product_data.csv")

# Convert product categories into numerical vectors
vectorizer = TfidfVectorizer()
product_tfidf_matrix = vectorizer.fit_transform(product_df["Similar_Product_List"])

# Save the model
model_path = "models/content_based_model.pkl"
with open(model_path, "wb") as f:
    pickle.dump(product_tfidf_matrix, f)

print(f"✅ Model saved successfully at: {model_path}")

def recommend_products(product_name, top_n=5):
    try:
        idx = product_df[product_df["Category"] == product_name].index[0]
    except IndexError:
        return f"❌ No products found for '{product_name}'"

    cosine_sim = cosine_similarity(product_tfidf_matrix, product_tfidf_matrix)
    similar_indices = cosine_sim[idx].argsort()[-top_n-1:-1][::-1]
    
    return product_df.iloc[similar_indices][["Product_ID", "Category", "Price"]]

# Example Usage
print(recommend_products("Shoes"))
