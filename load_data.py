# load_data.py
import pandas as pd
import sqlite3

# Load and clean customer data
customer_df = pd.read_csv("customer_data_collection.csv", on_bad_lines='skip')

# Clean column names
customer_df = customer_df.rename(columns={
    "Customer_ID": "id",
    "Age": "age",
    "Gender": "gender",
    "Location": "location",
    "Browsing_History": "browsing_history",
    "Purchase_History": "purchase_history",
    "Customer_Segment": "segment",
    "Avg_Order_Value": "avg_order_value",
    "Holiday": "holiday",
    "Season": "season"
})

# Optional: Strip the "C" from Customer_ID to make it integer, or keep it as text
customer_df["id"] = customer_df["id"].str.replace("C", "", regex=False).astype(int)

# Load and clean product data
product_df = pd.read_csv("product_recommendation_data.csv", on_bad_lines='skip')

product_df = product_df.rename(columns={
    "Product_ID": "id",
    "Category": "category",
    "Subcategory": "subcategory",
    "Price": "price",
    "Brand": "brand",
    "Average_Rating_of_Similar_Products": "avg_similar_rating",
    "Product_Rating": "product_rating",
    "Customer_Review_Sentiment_Score": "sentiment_score",
    "Holiday": "holiday",
    "Season": "season",
    "Geographical_Location": "location",
    "Similar_Product_List": "similar_products",
    "Probability_of_Recommendation": "recommendation_prob"
})

# Strip 'P' from product IDs too
product_df["id"] = product_df["id"].str.replace("P", "", regex=False).astype(int)

# Insert into SQLite
conn = sqlite3.connect("ecomm.db")

customer_df.to_sql("customers", conn, if_exists="replace", index=False)
product_df.to_sql("products", conn, if_exists="replace", index=False)

conn.close()

print("✅ Data inserted into SQLite successfully.")
