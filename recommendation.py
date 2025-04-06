from flask import Flask, request, jsonify
import pickle
import threading
import gradio as gr
from collaborative_filtering import recommend_for_customer

app = Flask(__name__)

# Load models with error handling
try:
    with open("models/content_based_model.pkl", "rb") as f:
        content_based_model = pickle.load(f)
    with open("models/collaborative_model.pkl", "rb") as f:
        collaborative_model = pickle.load(f)
except Exception as e:
    print(f"Error loading models: {e}")

@app.route("/recommend", methods=["GET"])
def recommend():
    customer_id = request.args.get("customer_id")
    if not customer_id:
        return jsonify({"error": "customer_id is required"}), 400

    print(f"Received request for customer: {customer_id}")

    try:
        recommended_products = recommend_for_customer(customer_id)
        print(f"Full Recommendations for {customer_id}: {recommended_products}")  # Debugging

        return jsonify({"customer_id": customer_id, "recommendations": recommended_products})
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Welcome to the Recommendation API! Gradio UI is available at: <a href='http://127.0.0.1:7860' target='_blank'>Gradio UI</a>"

# Gradio Function
def gradio_recommend(customer_id):
    if not customer_id.strip():
        return "Please enter a valid Customer ID"

    try:
        recommendations = recommend_for_customer(customer_id)
        if "error" in recommendations:
            return recommendations["error"]
        if not recommendations:
            return "No recommendations found."
        
        return "\n".join([f"🛒 {item['Product_ID']} - {item['Category']} (${item['Price']})" for item in recommendations])
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize Gradio UI
interface = gr.Interface(
    fn=gradio_recommend,
    inputs=gr.Textbox(label="Enter Customer ID"),
    outputs=gr.Textbox(label="Recommended Products"),
    title="🛍️ Personalized Shopping Recommendations",
    description="Enter a Customer ID to get product recommendations."
)

# Run Gradio in a separate thread
def run_gradio(): # Change share=True if you want a public link
    interface.launch(server_name="127.0.0.1", server_port=7860, share=True)


if __name__ == "__main__":
    threading.Thread(target=run_gradio, daemon=False).start()  # Ensure Gradio runs properly
    app.run(debug=True, port=5000, use_reloader=False)  # Prevent multiple instances