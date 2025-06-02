from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from src.model import StockPriceModel, feature_columns

app = FastAPI()
model = StockPriceModel("model/model.keras", "model/scaler.pkl")


class PredictRequest(BaseModel):
    features: List[float]


@app.post("/predict")
def predict_price(request: PredictRequest):
    try:
        if len(request.features) != len(feature_columns):
            return {"error": f"Expected {len(feature_columns)} features: {feature_columns}"}
        prediction = model.predict(request.features)
        return {"predicted_price": round(prediction, 2)}
    except Exception as e:
        return {"error": str(e)}
