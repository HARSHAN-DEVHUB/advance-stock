#!/usr/bin/env python3
"""
Standalone Prediction Script
Uses the centralized DataManager for predictions.
"""

import sys
import os
from data_manager import DataManager
from config import DEFAULT_SYMBOL

def main():
    """Make a prediction using the latest data"""
    print("🔮 Stock Prediction Script")
    print("==========================")
    
    # Initialize data manager
    data_manager = DataManager()
    
    if data_manager.model is None:
        print("❌ No model found. Run training first:")
        print("   python start.py  # This will train the model")
        sys.exit(1)
    
    # Sample prediction data (replace with your values)
    sample_data = {
        "Daily Change %": 2.5,
        "Volatility": 3.2,
        "MA_5": 150.0,
        "MA_10": 148.5,
        "MA_20": 145.0,
        "Momentum": 5.0,
        "Volume_Change": 0.1,
        "RSI_14": 65.0
    }
    
    result, confidence = data_manager.predict(sample_data)
    
    if result:
        print(f"📈 Prediction: {result}")
        print(f"📊 Confidence: {confidence:.2%}")
    else:
        print(f"❌ Prediction failed: {confidence}")

if __name__ == "__main__":
    main()