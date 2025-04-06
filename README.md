# E-commerce-Recommendation
Personalized Shopping Recommendation System

A machine learning–powered product recommendation system for an e-commerce platform. This project uses both content-based filtering and collaborative filtering techniques to recommend products to users. It features a Flask backend and a Gradio-based frontend UI for real-time testing.

Features

- Content-Based Filtering: Suggests items similar to user interests  
- Collaborative Filtering (KNN): Suggests items based on similar customer behavior  
- REST API (Flask): For integrating with other platforms  
- Frontend (Gradio): Easy-to-use web UI for testing recommendations  
- ML Models: Trained using scikit-learn and pandas  
- Data-Driven: Uses real-world-style customer, browsing, and product data  

Folder Structure

├── api/
│   ├── app.py
│   ├── collaborative_filtering.py
│   └── content_based_model.pkl
├── data/
│   ├── cleaned_customer_data.csv
│   ├── cleaned_product_data.csv
├── models/
│   ├── content_based_model.pkl
│   └── collaborative_model.pkl
├── README.md
└── requirements.txt

Requirements

Install dependencies using:

pip install -r requirements.txt

Main libraries used:

- Flask  
- Gradio  
- pandas  
- scikit-learn  
- scipy  
- pickle  

How to Run

Start the app:

python api/app.py

- Gradio UI runs at: http://127.0.0.1:7860  
- Flask API runs at: http://127.0.0.1:5000  

API Usage

Example:
GET /recommend?customer_id=C1001

How it Works

1. Collaborative filtering uses KNN to find similar users based on their browsing and order data  
2. Recommendations are generated from products purchased by similar users  
3. If category matching fails, fallback to product name matching  
4. The system is wrapped with Gradio to allow user-friendly input of customer IDs  

Example Output

Input: C1002  
Output:  
P101 - Electronics ($199)  
P205 - Fitness ($89)  

Future Improvements

- Add product image previews  
- Build a hybrid recommendation model  
- Deploy the app to cloud platforms  
- Add user login and session tracking  

Inspiration

Inspired by platforms like Amazon and Myntra, this project demonstrates how personalization enhances shopping experiences.

Let me know if you want a downloadable `.md` file or if you want to tweak anything else!
