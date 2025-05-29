import pandas as pd

def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw stock price DataFrame by:
    - Removing first row if 'Date' column's first value is invalid
    - Converting price and volume columns to numeric types
    - Converting 'Date' column to datetime and setting it as index

    Args:
        df (pd.DataFrame): Raw DataFrame containing stock price data with a 'Date' column.

    Returns:
        pd.DataFrame: Cleaned DataFrame with 'Date' as datetime index and numeric columns.
    """
    first_date = str(df.iloc[0]['Date'])
    if not first_date.startswith("202"):
        df = df.drop(index=0).reset_index(drop=True)

    numeric_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    return df
