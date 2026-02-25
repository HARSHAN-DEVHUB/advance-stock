# Stock Prediction API - Backend

Production-ready FastAPI backend for stock price prediction using advanced machine learning and technical analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Alpha Vantage API Key (free at [alphavantage.co](https://www.alphavantage.co/))

### Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment** (Required):
   ```bash
   cp env_example.txt .env
   # Edit .env with your actual credentials
   ```

3. **Start Application**:
   ```bash
   python start.py
   ```

## 🛡️ Security Features

- ✅ **No hardcoded secrets** - All credentials via environment variables
- ✅ **Startup validation** - App fails fast if required env vars missing  
- ✅ **Input sanitization** - Pydantic validation with proper ranges
- ✅ **Proper error handling** - Appropriate HTTP status codes (404, 422, 500)

## 📊 API Endpoints

### Core Endpoints
- `GET /health` - Health check with model status
- `GET /status` - Detailed application status
- `POST /predict/` - Make prediction (with input validation)

### Data Management
- `GET /data/latest` - Get recent stock data
- `GET /data/processed` - Get processed data with features
- `POST /data/fetch` - Manual data fetch

### Model Operations  
- `POST /pipeline/run` - Complete pipeline (fetch + preprocess + train)
- `POST /model/train` - Train model only

### Input Validation
All prediction inputs have strict validation:
```json
{
  "Daily_Change": -50.0,    // -50% to +50%
  "Volatility": 0.0,        // 0% to 100%  
  "MA_5": 1.0,              // Must be positive
  "MA_10": 1.0,             // Must be positive
  "MA_20": 1.0,             // Must be positive
  "Momentum": -1000.0,      // -1000 to +1000
  "Volume_Change": -10.0,   // -1000% to +1000%
  "RSI_14": 0.0             // 0 to 100
}
```

## 🔄 Resilience Features

### API Reliability
- **Automatic retries** with exponential backoff for Alpha Vantage API
- **30-second timeouts** on all external API calls
- **Rate limit handling** with appropriate error messages
- **Data quality validation** before processing

### Error Handling
- **HTTP 404**: Data not found (run `/data/fetch` first)
- **HTTP 422**: Invalid input data (check validation ranges) 
- **HTTP 503**: Model not loaded (run `/pipeline/run` first)
- **HTTP 500**: Unexpected errors (check logs)

## 💾 Data Pipeline

### Flow
1. **Fetch**: Download daily OHLCV data from Alpha Vantage
2. **Validate**: Check data quality and completeness
3. **Preprocess**: Calculate technical indicators (MA, RSI, etc.)
4. **Train**: XGBoost classification model
5. **Serve**: Load model for predictions

### Storage
- Raw data: `../data/{symbol}_stock_data.csv`
- Processed data: `../data/{symbol}_stock_data_processed.csv`  
- Model: `../data/stock_prediction_model.pkl`
- Scaler: `../data/scaler.pkl`

## 🐳 Deployment

### Local Development
```bash
python start.py
```

### Docker (Production)
```bash
# Using docker-compose (recommended)
docker-compose up -d

# Manual docker build
docker build -t stock-api . 
docker run -p 8000:8000 --env-file .env stock-api
```

### Cloud Deployment
```bash
# Deploy script with multiple options
./deploy.sh docker  # Docker deployment
./deploy.sh local   # Local deployment
```

## 🗂 Scripts

All scripts now use the centralized `DataManager`:

- `python predict.py` - Make standalone predictions
- `python train_model.py [symbol]` - Train model for symbol
- `python data_fetch.py [symbol]` - Fetch data for symbol  
- `python preprocess.py [symbol]` - Preprocess data for symbol
- `python test_api.py` - Test all API endpoints

## 🔍 Troubleshooting

### Environment Issues
```bash
# Missing API key error
echo "ALPHA_VANTAGE_API_KEY=your_key" >> .env

# Validation error on startup 
cp env_example.txt .env  # Then edit with real values
```

### Model Issues  
```bash
# Model not found (503 error)
curl -X POST http://localhost:8000/pipeline/run

# Training failures
# Check logs for specific errors (API limits, data quality, etc.)
```

### API Issues
```bash
# Test API health
curl http://localhost:8000/health

# Check detailed status
curl http://localhost:8000/status

# Run test suite
python test_api.py
```

### Data Quality
- API automatically retries failed requests
- Data validation prevents corrupt datasets
- Check logs for specific Alpha Vantage errors

## 🎨 Architecture

```
FastAPI App → DataManager → Alpha Vantage API
     │              │
     ▼              ▼  
 Input Validation   Data Storage
 Error Handling    Model Cache
```

**Production Ready**: Security, reliability, and monitoring built-in. 