from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from datetime import datetime
import os
import pandas as pd
from data_manager import DataManager
from config import DEFAULT_SYMBOL, DATA_DIR, SUPPORTED_SYMBOLS

app = FastAPI(title="Stock Prediction API", version="1.0.0")

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data manager
data_manager = DataManager()

class StockData(BaseModel):
    Daily_Change: float = Field(..., ge=-50, le=50, description="Daily change percentage (-50% to +50%)")
    Volatility: float = Field(..., ge=0, le=100, description="Volatility percentage (0% to 100%)")
    MA_5: float = Field(..., gt=0, description="5-day moving average (must be positive)")
    MA_10: float = Field(..., gt=0, description="10-day moving average (must be positive)")
    MA_20: float = Field(..., gt=0, description="20-day moving average (must be positive)")
    Momentum: float = Field(..., ge=-1000, le=1000, description="Price momentum (-1000 to +1000)")
    Volume_Change: float = Field(..., ge=-10, le=10, description="Volume change ratio (-1000% to +1000%)")
    RSI_14: float = Field(..., ge=0, le=100, description="RSI indicator (0 to 100)")

class PipelineRequest(BaseModel):
    symbol: str = DEFAULT_SYMBOL

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    print("🚀 Starting Stock Prediction API...")
    print("✅ API is ready for predictions!")
    print("📊 You can manually trigger data updates and model training via API endpoints")

@app.get("/")
async def home():
    """API home endpoint"""
    return {
        "message": "📈 Stock Prediction API is running!",
        "version": "1.0.0",
        "status": "active",
        "last_update": data_manager.last_update.isoformat() if data_manager.last_update else None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = data_manager.model is not None and data_manager.scaler is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "last_update": data_manager.last_update.isoformat() if data_manager.last_update else None,
        "scheduler_running": False  # Manual mode
    }

@app.get("/data/latest")
async def get_latest_data(symbol: str = DEFAULT_SYMBOL):
    """Get the last 3 days of stock data in clean format"""
    try:
        # Check if data file exists
        data_file = os.path.join(DATA_DIR, f"{symbol}_stock_data.csv")
        if not os.path.exists(data_file):
            raise HTTPException(status_code=404, detail=f"No data found for {symbol}. Run /data/fetch first.")
        
        # Load the data
        df = pd.read_csv(data_file, index_col=0, parse_dates=True)
        
        # Get last 3 days
        latest_data = df.tail(3)
        
        # Format the data with full decimal precision
        formatted_data = []
        for date, row in latest_data.iterrows():
            formatted_row = {
                "date": str(date)[:10],  # Get YYYY-MM-DD format
                "open": f"{row['Open']:.8f}",
                "high": f"{row['High']:.8f}",
                "low": f"{row['Low']:.8f}",
                "close": f"{row['Close']:.8f}",
                "volume": f"{row['Volume']:.2f}",
                "daily_change_percent": f"{row['Daily Change %']:.8f}",
                "volatility": f"{row['Volatility']:.8f}"
            }
            formatted_data.append(formatted_row)
        
        return {
            "symbol": symbol,
            "last_updated": data_manager.last_update.isoformat() if data_manager.last_update else None,
            "data_points": len(df),
            "latest_3_days": formatted_data
        }
        
    except HTTPException:
        raise  # Let FastAPI handle HTTP exceptions
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No data found for {symbol}. Run /data/fetch first.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=422, detail=f"Data file for {symbol} is empty or corrupted.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error fetching data: {str(e)}")

@app.get("/data/processed")
async def get_processed_data(symbol: str = DEFAULT_SYMBOL):
    """Get the last 3 days of processed data (with features)"""
    try:
        # Check if processed data file exists
        processed_file = os.path.join(DATA_DIR, f"{symbol}_stock_data_processed.csv")
        if not os.path.exists(processed_file):
            raise HTTPException(status_code=404, detail=f"No processed data found for {symbol}. Run /pipeline/run first.")
        
        # Load the processed data
        df = pd.read_csv(processed_file, index_col=0, parse_dates=True)
        
        # Get last 3 days
        latest_data = df.tail(3)
        
        # Format the data with full decimal precision
        formatted_data = []
        for date, row in latest_data.iterrows():
            formatted_row = {
                "date": str(date)[:10],  # Get YYYY-MM-DD format
                "open": f"{row['Open']:.8f}",
                "high": f"{row['High']:.8f}",
                "low": f"{row['Low']:.8f}",
                "close": f"{row['Close']:.8f}",
                "volume": f"{row['Volume']:.2f}",
                "daily_change_percent": f"{row['Daily Change %']:.8f}",
                "volatility": f"{row['Volatility']:.8f}",
                "ma_5": f"{row['MA_5']:.8f}",
                "ma_10": f"{row['MA_10']:.8f}",
                "ma_20": f"{row['MA_20']:.8f}",
                "momentum": f"{row['Momentum']:.8f}",
                "volume_change": f"{row['Volume_Change']:.8f}",
                "rsi_14": f"{row['RSI_14']:.8f}"
            }
            formatted_data.append(formatted_row)
        
        return {
            "symbol": symbol,
            "last_updated": data_manager.last_update.isoformat() if data_manager.last_update else None,
            "data_points": len(df),
            "latest_3_days_processed": formatted_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching processed data: {str(e)}")

@app.post("/predict/")
async def predict(data: StockData):
    """Make a stock prediction"""
    if data_manager.model is None or data_manager.scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please run training first.")
    
    try:
        # Prepare input data
        input_data = {
            "Daily Change %": data.Daily_Change,
            "Volatility": data.Volatility,
            "MA_5": data.MA_5,
            "MA_10": data.MA_10,
            "MA_20": data.MA_20,
            "Momentum": data.Momentum,
            "Volume_Change": data.Volume_Change,
            "RSI_14": data.RSI_14
        }
        
        # Make prediction
        result, confidence = data_manager.predict(input_data)
        
        if result is None:
            raise HTTPException(status_code=500, detail=confidence)
        
        return {
            "prediction": result,
            "confidence": f"{confidence:.2%}",
            "timestamp": datetime.now().isoformat(),
            "features_used": list(input_data.keys())
        }
        
    except HTTPException:
        raise  # Let FastAPI handle HTTP exceptions
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected prediction error: {str(e)}")

@app.post("/pipeline/run")
async def run_pipeline(request: PipelineRequest):
    """Manually run the complete pipeline"""
    try:
        success = data_manager.update_pipeline(request.symbol)
        if success:
            return {
                "message": "Pipeline completed successfully",
                "symbol": request.symbol,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Pipeline failed")
    except HTTPException:
        raise  # Let FastAPI handle HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected pipeline error: {str(e)}")

@app.post("/data/fetch")
async def fetch_data(request: PipelineRequest):
    """Manually fetch new data"""
    try:
        df = data_manager.fetch_stock_data(request.symbol)
        if df is not None:
            return {
                "message": "Data fetched successfully",
                "symbol": request.symbol,
                "rows": len(df),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Data fetch failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data fetch error: {str(e)}")

@app.post("/preprocess")
async def preprocess_data(request: PipelineRequest):
    """Manually preprocess data"""
    try:
        df = data_manager.preprocess_data(request.symbol)
        if df is not None:
            return {
                "message": "Data preprocessed successfully",
                "symbol": request.symbol,
                "rows": len(df),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Data preprocessing failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preprocessing error: {str(e)}")

@app.post("/model/train")
async def train_model(request: PipelineRequest):
    """Manually train the model"""
    try:
        success = data_manager.train_model(request.symbol)
        if success:
            return {
                "message": "Model trained successfully",
                "symbol": request.symbol,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=500, detail="Model training failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")

@app.get("/status")
async def get_status():
    """Get detailed application status"""
    return {
        "api_status": "running",
        "model_loaded": data_manager.model is not None,
        "scaler_loaded": data_manager.scaler is not None,
        "last_update": data_manager.last_update.isoformat() if data_manager.last_update else None,
        "scheduler_running": False,  # Manual mode
        "scheduled_jobs": 0,  # Manual mode
        "supported_symbols": SUPPORTED_SYMBOLS,
        "default_symbol": DEFAULT_SYMBOL,
        "note": "Running in manual mode - use endpoints to trigger operations"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
