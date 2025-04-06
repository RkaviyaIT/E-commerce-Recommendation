# agents/product_agent.py

import sqlite3
import ast

def get_matching_products(customer_profile, db_path="ecomm.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Extract preferences
    preferences = ast.literal_eval(customer_profile["browsing_history"])

    query = "SELECT * FROM products WHERE Category IN ({})".format(
        ",".join(["?"] * len(preferences))
    )
    cursor.execute(query, preferences)
    rows = cursor.fetchall()
    conn.close()

    columns = ["Product_ID", "Category", "Subcategory", "Price", "Brand", 
               "Avg_Rating", "Rating", "Sentiment", "Holiday", "Season", 
               "Location", "Similar_Products", "Reco_Probability"]

    return [dict(zip(columns, row)) for row in rows]
