#!/usr/bin/env python3
"""
Stock Prediction API Startup Script
This script initializes the application and runs the initial pipeline setup.
"""

import os
import sys
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager
from config import *

def main():
    """Main startup function"""
    print("🚀 Starting Stock Prediction Application...")
    print(f"📅 Started at: {datetime.now()}")
    print(f"📊 Default symbol: {DEFAULT_SYMBOL}")
    print(f"📁 Data directory: {DATA_DIR}")
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Check if model exists, if not run initial pipeline
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("🔧 No existing model found. Running initial pipeline...")
        
        success = data_manager.update_pipeline(DEFAULT_SYMBOL)
        if success:
            print("✅ Initial pipeline completed successfully!")
        else:
            print("❌ Initial pipeline failed!")
            print("⚠️ You can still start the API, but predictions won't work until training is complete.")
    else:
        print("✅ Existing model found. Loading...")
        data_manager.load_model()
        print("✅ Model loaded successfully!")
    
    print("📊 Manual Mode: Use API endpoints to trigger operations:")
    print("   - POST /pipeline/run - Run complete pipeline")
    print("   - POST /data/fetch - Fetch new data")
    print("   - POST /model/train - Train model")
    print("   - POST /predict/ - Make predictions")
    
    # Start the FastAPI application
    print("🌐 Starting FastAPI server...")
    import uvicorn
    from app import app
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main() 