import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

# Load customer and product data
customer_df = pd.read_csv(r"C:\Users\Admin\OneDrive\Desktop\e-commerce\data\customer_data.csv")
product_df = pd.read_csv(r"C:\Users\Admin\OneDrive\Desktop\e-commerce\data\product_data.csv")

# Fill missing values with empty strings
customer_df.fillna("", inplace=True)
product_df.fillna("", inplace=True)

# Convert categorical features to numbers (Label Encoding)
encoder = LabelEncoder()
customer_df["Gender"] = encoder.fit_transform(customer_df["Gender"])
customer_df["Location"] = encoder.fit_transform(customer_df["Location"])

# Convert list columns into strings
customer_df["Browsing_History"] = customer_df["Browsing_History"].apply(lambda x: " ".join(eval(x)) if isinstance(x, str) else x)
product_df["Similar_Product_List"] = product_df["Similar_Product_List"].apply(lambda x: " ".join(eval(x)) if isinstance(x, str) else x)
os.makedirs("data", exist_ok=True)
# Save cleaned data
customer_df.to_csv("data/cleaned_customer_data.csv", index=False)
product_df.to_csv("data/cleaned_product_data.csv", index=False)

print("✅ Data Preprocessing Done!")
