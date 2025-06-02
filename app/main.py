from datetime import datetime, timedelta
from src.utils import clean_stock_data
from src.model import StockPriceModel, feature_columns
from src.utils import get_last_run_time, save_current_run_time
from src.data_crawler import update_stock_data


def main():
    # === Config ===
    ticker = "TSLA"
    data_path = f"data/daily_updates/{ticker}.csv"
    model_path = "model/model.keras"
    scaler_path = "model/scaler.pkl"

    # === Kiểm tra lần chạy gần nhất ===
    last_run = get_last_run_time()
    if last_run:
        delta = datetime.now() - last_run
        print(f"Last run: {delta.days} days, {delta.seconds // 3600} hours ago.")
        if delta < timedelta(hours=6):
            print("Skipped: already ran recently.")
            return

    # === Cập nhật dữ liệu ===
    df_updated = update_stock_data(ticker=ticker,
                                   file_path=data_path,
                                   window_size=60)
    if df_updated.empty:
        print("No data to predict.")
        return

    # === Làm sạch dữ liệu ===
    df_clean = clean_stock_data(df_updated)

    # === Lấy dòng dữ liệu mới nhất để dự đoán ===
    latest_row = df_clean.iloc[-1]
    features = [latest_row[col] for col in feature_columns]

    # === Dự đoán ===
    print("Predicting with latest data...")
    model = StockPriceModel(model_path, scaler_path)
    prediction = model.predict(features)
    print(f"Predicted price for {ticker} (next day): ${prediction:.2f}")

    # === Cập nhật thời gian chạy ===
    save_current_run_time()


if __name__ == "__main__":
    main()
