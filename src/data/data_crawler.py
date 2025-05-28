import yfinance as yf
import pandas as pd
import os

def crawl_stock_data(ticker="AAPL", start="2020-01-01", end="2024-12-31", output_path="data/raw"):
    data = yf.download(ticker, start=start, end=end, interval="1d")

    if data.empty:
        print(f"No data found for {ticker}.")
        return

    # Reset index để Date thành cột bình thường thay vì index
    data.reset_index(inplace=True)

    os.makedirs(output_path, exist_ok=True)
    filename = f"{ticker}_{start}_{end}.csv".replace(":", "-")
    data.to_csv(os.path.join(output_path, filename), index=False)
    print(f"Saved {ticker} data to {output_path}/{filename}")

if __name__ == "__main__":
    ticker = "TSLA"
    start_date = "2020-01-01"
    end_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    output_path = "data/raw"
    crawl_stock_data(ticker=ticker, start=start_date, end=end_date)
