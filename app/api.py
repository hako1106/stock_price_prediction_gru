from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from src.model import StockPriceModel

app = FastAPI()
model = StockPriceModel("model/model.keras", "model/scaler.pkl")

class PredictRequest(BaseModel):
    features: List[float]

@app.post("/predict")
def predict_price(request: PredictRequest):
    prediction = model.predict(request.features)
    return {"predicted_price": round(prediction, 2)}
