#!/usr/bin/env python3
"""
Standalone Data Preprocessing Script
Uses the centralized DataManager for preprocessing.
"""

import sys
from data_manager import DataManager
from config import DEFAULT_SYMBOL

def main():
    """Preprocess stock data using the centralized pipeline"""
    print("🔧 Data Preprocessing Script")
    print("============================")
    
    # Initialize data manager
    data_manager = DataManager()
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SYMBOL
    print(f"📊 Preprocessing data for: {symbol}")
    
    # Preprocess data only
    df = data_manager.preprocess_data(symbol)
    
    if df is not None:
        print(f"✅ Successfully preprocessed {len(df)} rows")
        print(f"📊 Features available: {list(df.columns)}")
    else:
        print("❌ Preprocessing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
