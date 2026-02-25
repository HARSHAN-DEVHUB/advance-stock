#!/usr/bin/env python3
"""
Standalone Data Fetching Script
Uses the centralized DataManager for data fetching.
"""

import sys
from data_manager import DataManager
from config import DEFAULT_SYMBOL

def main():
    """Fetch stock data using the centralized pipeline"""
    print("📊 Data Fetching Script")
    print("=======================")
    
    # Initialize data manager
    data_manager = DataManager()
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SYMBOL
    print(f"📈 Fetching data for: {symbol}")
    
    # Fetch data only
    df = data_manager.fetch_stock_data(symbol)
    
    if df is not None:
        print(f"✅ Successfully fetched {len(df)} days of data")
        print(f"📅 Date range: {df.index.min()} to {df.index.max()}")
    else:
        print("❌ Data fetch failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
