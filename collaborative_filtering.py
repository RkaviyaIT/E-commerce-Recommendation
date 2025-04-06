import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import pickle
import ast  # Safe parsing of purchase history

# Load customer data
customer_df = pd.read_csv("data/cleaned_customer_data.csv")

# Load product data
product_df = pd.read_csv("data/cleaned_product_data.csv")

# Create User-Item Matrix
customer_product_matrix = customer_df.pivot(
    index="Customer_ID",
    columns="Browsing_History",
    values="Avg_Order_Value"
).fillna(0)

# Convert to sparse matrix
sparse_matrix = csr_matrix(customer_product_matrix.values)

# Train KNN Model
knn = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=5)
knn.fit(sparse_matrix)

# Save the model
with open("models/collaborative_model.pkl", "wb") as f:
    pickle.dump(knn, f)

def recommend_for_customer(customer_id, top_n=5):
    if customer_id not in customer_product_matrix.index:
        return f"❌ Customer ID '{customer_id}' not found in the dataset."

    customer_idx = customer_product_matrix.index.get_loc(customer_id)
    distances, indices = knn.kneighbors(
        sparse_matrix[customer_idx].reshape(1, -1),
        n_neighbors=top_n + 1  # +1 to skip the user itself
    )

    print(f"🔍 Similar customers for {customer_id}: {[customer_product_matrix.index[i] for i in indices[0][1:]]}")

    # Optional mapping to match item names with product categories
    mapping = {
    "Non-fiction": "Books",
    "Fiction": "Books",
    "Biography": "Books",
    "Yoga Mat": "Fitness",
    "Jeans": "Fashion",
    "Jacket": "Fashion",
    "Shoes": "Fashion",
    "Treadmill": "Fitness",
    "Comics": "Books",
    "Smartphone": "Electronics"  # ✅ Add this line
}


    recommended_products = []

    for idx in indices[0][1:]:  # Skip the same customer
        similar_customer_id = customer_product_matrix.index[idx]
        history = customer_df[customer_df["Customer_ID"] == similar_customer_id]["Purchase_History"].fillna("[]").values[0]

        print(f"🛒 Customer {similar_customer_id} Purchase History: {history}")

        try:
            purchased_items = ast.literal_eval(history)
        except Exception as e:
            print(f"⚠️ Error parsing history for {similar_customer_id}: {e}")
            continue

        for item in purchased_items:
            mapped_item = mapping.get(item, item)
            matched = product_df[product_df["Category"].str.contains(mapped_item, case=False, na=False)]

            print(f"🔎 Products for '{item}' (as '{mapped_item}'): {matched[['Product_ID', 'Category', 'Price']].to_dict(orient='records')}")

            if not matched.empty:
                recommended_products.extend(
                    matched[["Product_ID", "Category", "Price"]].to_dict(orient="records")
                )

    # Remove duplicates while preserving order
    seen = set()
    unique_recommendations = []
    for product in recommended_products:
        pid = product["Product_ID"]
        if pid not in seen:
            seen.add(pid)
            unique_recommendations.append(product)
        if len(unique_recommendations) >= top_n:
            break

    return unique_recommendations

# 🧪 Optional Test
if __name__ == "__main__":
    recs = recommend_for_customer("C1002", top_n=5)
    for r in recs:
        print(f"🛍️ {r['Product_ID']} - {r['Category']} (${r['Price']})")
print(customer_df[customer_df["Customer_ID"] == "C1002"]["Purchase_History"])


recs = recommend_for_customer("C1002", top_n=5)
if not recs:
    print("⚠️ No recommendations found. Let's debug 👇")

    # Check if customer exists
    if "C1002" not in customer_product_matrix.index:
        print("❌ Customer not found in matrix")

    # Check purchase history
    history = customer_df[customer_df["Customer_ID"] == "C1002"]["Purchase_History"].values
    print("🧾 Purchase History:", history)

    # Check categories in product_df
    print("🗂️ Product Categories Available:", product_df["Category"].unique())
else:
    for r in recs:
        print(f"✅ {r}")
