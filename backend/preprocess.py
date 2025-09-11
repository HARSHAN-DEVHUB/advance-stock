import pandas as pd
import numpy as np
import os

def preprocess_data(file_name):
    """Clean and prepare stock data for prediction"""
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    file_path = os.path.join(data_dir, file_name)
    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found!")
        return None
    # Load data
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    # Standardize column names
    column_mapping = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    }
    df.rename(columns=column_mapping, inplace=True, errors="ignore")
    # Ensure numeric data
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    # Basic features
    df["Daily Change %"] = (df["Close"] - df["Open"]) / df["Open"] * 100
    df["Volatility"] = (df["High"] - df["Low"]) / df["Open"] * 100
    df["MA_5"] = df["Close"].rolling(window=5).mean()
    df["MA_10"] = df["Close"].rolling(window=10).mean()
    # Advanced features
    df["MA_20"] = df["Close"].rolling(window=20).mean()
    df["Momentum"] = df["Close"] - df["Close"].shift(5)
    df["Volume_Change"] = df["Volume"].pct_change()
    # RSI_14 calculation
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / (avg_loss + 1e-9)  # avoid division by zero
    df["RSI_14"] = 100 - (100 / (1 + rs))
    # Clean infinities and fill missing values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.bfill(inplace=True)
    # Save processed data
    processed_file = os.path.join(data_dir, file_name.replace(".csv", "_processed.csv"))
    df.to_csv(processed_file)
    print(f"✅ Processed data saved: {processed_file}")
    return df

# Example Usage
if __name__ == "__main__":
    preprocess_data("INDUSINDBK.BSE_stock_data.csv")
