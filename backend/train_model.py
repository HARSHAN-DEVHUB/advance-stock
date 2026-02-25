#!/usr/bin/env python3
"""
Standalone Model Training Script
Uses the centralized DataManager for training.
"""

import sys
import os
from data_manager import DataManager
from config import DEFAULT_SYMBOL

def main():
    """Train the model using the centralized pipeline"""
    print("🤖 Model Training Script")
    print("========================")
    
    # Initialize data manager
    data_manager = DataManager()
    
    symbol = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SYMBOL
    print(f"📊 Training model for: {symbol}")
    
    # Run complete pipeline
    success = data_manager.update_pipeline(symbol)
    
    if success:
        print("✅ Training completed successfully!")
        print(f"📁 Model saved to data directory")
    else:
        print("❌ Training failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
