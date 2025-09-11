import requests
import pandas as pd
import os
import time

API_KEY = "2KQFY7C6QSGD56WA"
BASE_URL = "https://www.alphavantage.co/query"

def fetch_stock_data(symbol="INDUSINDBK.BSE"):
    """Fetch latest stock data for Indian stocks using Alpha Vantage"""
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if "Time Series (Daily)" not in data:
        print(f"❌ No data found for {symbol} or API limit reached.")
        return None

    ts_data = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(ts_data, orient="index")
    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Daily Change %"] = (df["Close"] - df["Open"]) / df["Open"] * 100
    df["Volatility"] = (df["High"] - df["Low"]) / df["Open"] * 100

    os.makedirs("./data", exist_ok=True)
    file_path = f"./data/{symbol}_stock_data.csv"
    df.to_csv(file_path)
    print(f"✅ Data saved: {file_path}")
    return df

# Example Usage
if __name__ == "__main__":
    fetch_stock_data("INDUSINDBK.BSE")  # Use BSE symbol for Indian stocks
