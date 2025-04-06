from agents.customer_agent import get_customer_profile
from agents.product_agent import get_matching_products

def recommend_products(customer_id):
    customer_profile = get_customer_profile(customer_id)
    if not customer_profile:
        return {"error": "Customer not found"}

    products = get_matching_products(customer_profile)

    # Rank by sentiment_score * recommendation_prob * product_rating
    for product in products:
        try:
            score = (float(product["sentiment_score"]) *
                     float(product["recommendation_prob"]) *
                     float(product["product_rating"]))
        except:
            score = 0
        product["score"] = score

    top_products = sorted(products, key=lambda x: x["score"], reverse=True)[:5]

    return {
        "customer_id": customer_id,
        "recommendations": [
            {
                "product_id": p["Product_ID"],
                "category": p["Category"],
                "subcategory": p["Subcategory"],
                 "price": p["Price"]

            } for p in top_products
        ]
    }
