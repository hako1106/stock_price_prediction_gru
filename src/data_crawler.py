import yfinance as yf
import pandas as pd
import os
from typing import Optional

def crawl_stock_data(
    ticker: str = "TSLA",
    start: str = "2020-01-01",
    end: Optional[str] = None,
    output_path: str = "data/raw"
) -> None:
    """
    Download historical daily stock data for a given ticker and date range,
    then save it as a CSV file in the specified directory.

    Args:
        ticker (str): Stock ticker symbol (e.g. "AAPL", "TSLA").
        start (str): Start date in "YYYY-MM-DD" format.
        end (Optional[str]): End date in "YYYY-MM-DD" format. If None, uses today's date.
        output_path (str): Directory path to save the downloaded CSV file.

    Returns:
        None
    """
    if end is None:
        end = pd.Timestamp.now().strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start, end=end, interval="1d")

    if data.empty:
        print(f"No data found for ticker '{ticker}' in the date range {start} to {end}.")
        return

    data.reset_index(inplace=True)

    os.makedirs(output_path, exist_ok=True)

    filename = f"{ticker}_{start}_{end}.csv".replace(":", "-")

    data.to_csv(os.path.join(output_path, filename), index=False)

    print(f"Saved data for ticker '{ticker}' to '{os.path.join(output_path, filename)}'")

if __name__ == "__main__":
    crawl_stock_data(ticker="TSLA", start="2020-01-01", end=None, output_path="data/raw")