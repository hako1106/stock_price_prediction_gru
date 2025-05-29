import os
import pandas as pd
from src.data_crawler import crawl_stock_data
from src.data_cleaner import clean_stock_data
from src.model import StockPriceModel

def main():
    # Config
    ticker = "TSLA"
    start_date = "2020-01-01"
    output_dir = "data/raw"
    model_path = "model/model.keras"
    scaler_path = "model/scaler.pkl"

    # Step 1: Crawl stock data
    print("Crawling data...")
    crawl_stock_data(ticker=ticker, start=start_date, end=None, output_path=output_dir)

    # Step 2: Load and clean data
    filename = f"{ticker}_{start_date}_{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv".replace(":", "-")
    file_path = os.path.join(output_dir, filename)
    df = pd.read_csv(file_path)
    df_clean = clean_stock_data(df)

    # Step 3: Extract features (last available row)
    latest_row = df_clean.iloc[-1]
    features = [latest_row[col] for col in ['Close']]  # Adjust based on model's input features

    # Step 4: Predict stock price
    print("Loading model and making prediction...")
    model = StockPriceModel(model_path, scaler_path)
    prediction = model.predict(features)

    # Step 5: Output result
    print(f"Predicted price for {ticker} on next day (based on last data): ${prediction:.2f}")

if __name__ == "__main__":
    main()
