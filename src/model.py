import joblib
import numpy as np
from keras.models import load_model
from typing import List

feature_columns = ['Close']


class StockPriceModel:
    def __init__(self, model_path: str, scaler_path: str):
        self.model = load_model(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, features: List[float]) -> float:
        if len(features) != len(feature_columns):
            raise ValueError(f"Expect {len(feature_columns)} features: {feature_columns}")

        x = np.array(features).reshape(1, -1)
        x_scaled = self.scaler.transform(x)
        pred = self.model.predict(x_scaled, verbose=0)

        return float(pred[0][0])


if __name__ == "__main__":
    model_path = "model/model.keras"
    scaler_path = "model/scaler.pkl"
    stock_model = StockPriceModel(model_path, scaler_path)

    # Example input features for prediction
    example_features = [720.5]
    prediction = stock_model.predict(example_features)
    print(f"Predicted price: {prediction:.2f}")
