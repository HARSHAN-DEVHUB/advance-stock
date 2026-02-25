import pandas as pd
import numpy as np
import requests
import os
import joblib
import time
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from config import *

class DataManager:
    def __init__(self):
        self.last_update = None
        self.model = None
        self.scaler = None
        self.load_model()
    
    def fetch_stock_data(self, symbol=DEFAULT_SYMBOL, max_retries=3, timeout=30):
        """Fetch latest stock data for Indian stocks using Alpha Vantage with retry logic"""
        print(f"📊 Fetching data for {symbol}...")
        
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": API_KEY
        }
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 Attempt {attempt + 1}/{max_retries}")
                response = requests.get(BASE_URL, params=params, timeout=timeout)
                response.raise_for_status()  # Raise exception for HTTP errors
                
                data = response.json()
                
                # Check for API errors
                if "Error Message" in data:
                    raise ValueError(f"API Error: {data['Error Message']}")
                if "Note" in data:
                    raise ValueError(f"API Rate Limit: {data['Note']}")
                if "Information" in data:
                    raise ValueError(f"API Info: {data['Information']}")
                
                if "Time Series (Daily)" not in data:
                    raise ValueError(f"No time series data found for {symbol}")

                ts_data = data["Time Series (Daily)"]
                if not ts_data:
                    raise ValueError(f"Empty time series data for {symbol}")
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
                
                # Validate data quality
                if df.isnull().all().any():
                    raise ValueError(f"Data contains all null values for some columns")
                    
                df["Daily Change %"] = (df["Close"] - df["Open"]) / df["Open"] * 100
                df["Volatility"] = (df["High"] - df["Low"]) / df["Open"] * 100

                file_path = os.path.join(DATA_DIR, f"{symbol}_stock_data.csv")
                df.to_csv(file_path)
                print(f"✅ Data saved: {file_path}")
                
                self.last_update = datetime.now()
                return df
                
            except (requests.RequestException, ValueError) as e:
                print(f"❌ Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ All {max_retries} attempts failed")
                    return None
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                return None

    def preprocess_data(self, symbol=DEFAULT_SYMBOL):
        """Clean and prepare stock data for prediction"""
        print(f"🔧 Preprocessing data for {symbol}...")
        
        file_path = os.path.join(DATA_DIR, f"{symbol}_stock_data.csv")
        if not os.path.exists(file_path):
            print(f"❌ Error: File {file_path} not found!")
            return None
            
        try:
            # Load data
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            
            # Standardize column names
            column_mapping = {
                "open": "Open", "high": "High", "low": "Low",
                "close": "Close", "volume": "Volume"
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
            rs = avg_gain / (avg_loss + 1e-9)
            df["RSI_14"] = 100 - (100 / (1 + rs))
            
            # Clean infinities and fill missing values
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.bfill(inplace=True)
            
            # Save processed data
            processed_file = os.path.join(DATA_DIR, f"{symbol}_stock_data_processed.csv")
            df.to_csv(processed_file)
            print(f"✅ Processed data saved: {processed_file}")
            return df
            
        except Exception as e:
            print(f"❌ Error preprocessing data: {e}")
            return None

    def train_model(self, symbol=DEFAULT_SYMBOL):
        """Train the prediction model"""
        print(f"🤖 Training model for {symbol}...")
        
        file_path = os.path.join(DATA_DIR, f"{symbol}_stock_data_processed.csv")
        if not os.path.exists(file_path):
            print(f"❌ Error: Processed data file not found: {file_path}")
            return False

        try:
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            
            # Clean the data
            df.replace([np.inf, -np.inf], np.nan, inplace=True)
            df.bfill(inplace=True)
            df = df.clip(lower=-1e6, upper=1e6)
            
            # Define the target: predict if next day's open > today's close
            df["Target"] = np.where(df["Open"].shift(-1) > df["Close"], 1, 0)
            
            # Ensure all required features are present
            missing_features = [f for f in FEATURES if f not in df.columns]
            if missing_features:
                print(f"❌ Missing features in dataset: {missing_features}")
                return False

            X = df[FEATURES]
            y = df["Target"]
            
            # Remove rows with NaN values
            mask = ~(X.isna().any(axis=1) | y.isna())
            X = X[mask]
            y = y[mask]
            
            if len(X) == 0:
                print("❌ No valid data for training")
                return False
            
            # Scale the features
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Save the scaler
            joblib.dump(scaler, SCALER_PATH)
            print(f"✅ Scaler saved: {SCALER_PATH}")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y, test_size=0.2, shuffle=False, random_state=42
            )
            
            # Train the XGBoost model
            model = xgb.XGBClassifier(
                n_estimators=150,
                learning_rate=0.05,
                use_label_encoder=False,
                eval_metric='logloss'
            )
            model.fit(X_train, y_train)
            
            # Save trained model
            joblib.dump(model, MODEL_PATH)
            print(f"✅ Model saved: {MODEL_PATH}")
            
            # Evaluate model
            y_pred = model.predict(X_test)
            accuracy = (y_pred == y_test).mean()
            print(f"📊 Model accuracy: {accuracy:.2%}")
            
            self.model = model
            self.scaler = scaler
            
            return True
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            return False

    def load_model(self):
        """Load the trained model and scaler"""
        try:
            if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
                self.model = joblib.load(MODEL_PATH)
                self.scaler = joblib.load(SCALER_PATH)
                print("✅ Model and Scaler loaded successfully.")
            else:
                print("⚠️ Model files not found. Run training first.")
        except Exception as e:
            print(f"❌ Error loading model: {e}")

    def predict(self, data):
        """Make a prediction using the loaded model"""
        if self.model is None or self.scaler is None:
            return None, "Model not loaded"
        
        try:
            # Prepare input
            input_df = pd.DataFrame([data])
            
            # Scale and predict
            input_scaled = self.scaler.transform(input_df)
            prediction = self.model.predict(input_scaled)[0]
            probability = self.model.predict_proba(input_scaled)[0]
            
            result = "Higher" if prediction == 1 else "Lower"
            confidence = max(probability)
            
            return result, confidence
            
        except Exception as e:
            return None, f"Prediction failed: {str(e)}"

    def update_pipeline(self, symbol=DEFAULT_SYMBOL):
        """Run the complete pipeline: fetch -> preprocess -> train"""
        print(f"🔄 Running complete pipeline for {symbol}...")
        
        # Fetch data
        df = self.fetch_stock_data(symbol)
        if df is None:
            return False
        
        # Preprocess data
        df = self.preprocess_data(symbol)
        if df is None:
            return False
        
        # Train model
        success = self.train_model(symbol)
        if success:
            print("✅ Pipeline completed successfully!")
        else:
            print("❌ Pipeline failed!")
        
        return success 