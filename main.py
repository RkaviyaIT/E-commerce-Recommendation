# main.py
from fastapi import FastAPI, HTTPException
from agents.reco_agent import recommend_products  # 👈 Import from agent-based reco logic

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the product recommendation API!"}

@app.get("/recommend/{customer_id}")
def recommend(customer_id: int):
    try:
        result = recommend_products(customer_id)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
