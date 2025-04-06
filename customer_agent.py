# agents/customer_agent.py

import sqlite3

def get_customer_profile(customer_id, db_path="ecomm.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    columns = ["id", "age", "gender", "location", "browsing_history",
               "purchase_history", "segment", "avg_order_value", "holiday", "season"]
    
    return dict(zip(columns, row))
