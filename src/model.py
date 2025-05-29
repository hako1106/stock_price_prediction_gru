import joblib
import numpy as np
from keras.models import load_model
from typing import List

class StockPriceModel:
    """
    A wrapper class for loading a trained Keras stock price prediction model
    and its corresponding scaler for preprocessing.

    Attributes:
        model (tf.keras.Model): Trained Keras model.
        scaler (sklearn.preprocessing object): Fitted scaler used for input normalization.
    """

    def __init__(self, model_path: str, scaler_path: str):
        """
        Initialize the StockPriceModel by loading the model and scaler.

        Args:
            model_path (str): Path to the saved Keras model (.keras or .h5 file).
            scaler_path (str): Path to the saved scaler object (.pkl file).
        """
        self.model = load_model(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, features: List[float]) -> float:
        """
        Make a stock price prediction based on input features.

        Args:
            features (List[float]): A list of numeric feature values.

        Returns:
            float: Predicted stock price.
        """
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