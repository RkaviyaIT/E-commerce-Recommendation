# recommendation_model.py
import sqlite3

def get_recommendations(customer_id: int):
    conn = sqlite3.connect("ecomm.db")
    cursor = conn.cursor()

    # Fetch customer's purchase history
    cursor.execute("SELECT purchase_history FROM customers WHERE id=?", (customer_id,))
    result = cursor.fetchone()
    if not result:
        return []

    # Parse purchased categories or products
    purchased = eval(result[0]) if result[0] else []

    # Example logic: Recommend similar category products not yet purchased
    cursor.execute("SELECT id, category, subcategory, price FROM products")
    products = cursor.fetchall()

    recommendations = []
    for pid, cat, subcat, price in products:
        if any(p.lower() in cat.lower() or p.lower() in subcat.lower() for p in purchased):
            recommendations.append({
                "product_id": pid,
                "category": cat,
                "subcategory": subcat,
                "price": price
            })

    conn.close()
    return recommendations[:5]  # Return top 5 for now
