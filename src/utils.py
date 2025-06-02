from datetime import datetime
import os
import pandas as pd


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    df.reset_index(inplace=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        df.columns.name = None

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df = df.dropna(subset=["Date", "Close"], how='any')
    df.drop_duplicates(subset=["Date"], keep='last', inplace=True)
    df.sort_values(by="Date", inplace=True)

    return df


def get_last_run_time(file_path="last_run.txt") -> datetime | None:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            timestamp_str = f.read().strip()
            try:
                return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
    return None


def save_current_run_time(file_path="last_run.txt") -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, "w") as f:
        f.write(now)
