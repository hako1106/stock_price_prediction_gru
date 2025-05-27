import pandas as pd

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)

    first_date = str(df.iloc[0]['Date'])
    if not first_date.startswith("202"):
        df = df.drop(index=0).reset_index(drop=True)

    numeric_cols = ['Close', 'High', 'Low', 'Open', 'Volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    return df

def check_missing_values(df):
    return df.isnull().sum()[df.isnull().sum() > 0]

def save_clean_data(df, output_path):
    df.to_csv(output_path, index=True, index_label="Date")

if __name__ == "__main__":
    input_path = "data/raw/TSLA_2020-01-01_2025-05-27.csv"
    output_path = "data/processed/tsla_processed.csv"

    df = load_and_clean_data(input_path)
    print("Missing values:\n", check_missing_values(df))
    save_clean_data(df, output_path)
