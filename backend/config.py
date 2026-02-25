import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
if not API_KEY:
    raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is required")
BASE_URL = "https://www.alphavantage.co/query"

# Stock Configuration
DEFAULT_SYMBOL = "INDUSINDBK.BSE"
SUPPORTED_SYMBOLS = [
    "INDUSINDBK.BSE",
    "RELIANCE.BSE", 
    "TCS.BSE",
    "HDFCBANK.BSE",
    "INFY.BSE"
]

# Data Configuration
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
MODEL_PATH = os.path.join(DATA_DIR, "stock_prediction_model.pkl")
SCALER_PATH = os.path.join(DATA_DIR, "scaler.pkl")

# Model Configuration
FEATURES = [
    "Daily Change %", "Volatility", "MA_5", "MA_10",
    "MA_20", "Momentum", "Volume_Change", "RSI_14"
]

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True) 