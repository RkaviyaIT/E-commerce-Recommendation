# setup_db.py
import sqlite3

conn = sqlite3.connect("ecomm.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    location TEXT,
    browsing_history TEXT,
    purchase_history TEXT,
    segment TEXT,
    avg_order_value REAL,
    holiday TEXT,
    season TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    category TEXT,
    subcategory TEXT,
    price REAL,
    brand TEXT,
    avg_similar_rating REAL,
    product_rating REAL,
    sentiment_score REAL,
    holiday TEXT,
    season TEXT,
    location TEXT,
    similar_products TEXT,
    recommendation_prob REAL
)
''')

conn.commit()
conn.close()

print("✅ Tables created.")
