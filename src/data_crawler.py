import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional
from utils import clean_stock_data

def crawl_stock_data(
    ticker: str = "TSLA",
    start: str = "2020-01-01",
    end: Optional[str] = None,
    output_path: str = None
) -> pd.DataFrame:
    
    if end is None:
        end = pd.Timestamp.today().strftime('%Y-%m-%d')

    print(f"Downloading {ticker} data from {start} to {end}...")
    df = yf.download(ticker, start=start, end=end, interval="1d")

    if df.empty:
        print(f"[Warning] No data found for {ticker} from {start} to {end}.")
        return pd.DataFrame()

    df = clean_stock_data(df)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"[Saved] Data for {ticker} saved to {output_path}")

    return df


def update_stock_data(
        ticker: str = "TSLA",
        file_path: str = None,
        window_size: int = 60
) -> pd.DataFrame:
    
    if file_path is None:
        file_path = f"data/daily_updates/{ticker}.csv"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)
        df_old['Date'] = pd.to_datetime(df_old['Date'])
    else:
        df_old = pd.DataFrame()

    if not df_old.empty:
        last_date = df_old['Date'].max()
        start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        start_date = (datetime.today() - timedelta(days=window_size)).strftime('%Y-%m-%d')

    end_date = datetime.today().strftime('%Y-%m-%d')

    if start_date >= end_date:
        print("Data is already up to date.")
        return df_old

    print(f"Downloading data from {start_date} to {end_date}...")
    df_new = yf.download(ticker, start=start_date, end=end_date, interval='1d')

    if df_new.empty:
        print("No new data downloaded.")
        return df_old

    df_new = clean_stock_data(df_new)

    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    df_combined.drop_duplicates(subset='Date', keep='last', inplace=True)
    df_combined.sort_values(by='Date', inplace=True)

    df_combined.to_csv(file_path, index=False)
    print(f"Updated {ticker} data to {file_path}")
    return df_combined
