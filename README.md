# Stock Prediction API

A production-ready FastAPI application that predicts stock opening prices using machine learning. The application fetches data, preprocesses technical indicators, trains XGBoost models, and provides predictions via secure REST API endpoints.

## Features

- 🤖 **Intelligent Data Fetching**: Robust Alpha Vantage API integration with retry logic and exponential backoff
- 🔧 **Advanced Preprocessing**: Technical indicators (MA, RSI, momentum, volatility) with data validation
- 🎯 **ML Model Training**: XGBoost classification with proper error handling
- 🔐 **Security First**: Environment-based configuration, no hardcoded secrets
- 🛡️ **Input Validation**: Pydantic models with range validation for all prediction inputs
- 🌐 **Reliable REST API**: Proper HTTP status codes, structured error responses
- 📊 **Health Monitoring**: Comprehensive health checks and status endpoints
- 🔄 **Resilient Architecture**: Timeout handling, retry mechanisms, graceful degradation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables (Required)

Copy `env_example.txt` to `.env` and configure all required variables:

```bash
cp backend/env_example.txt backend/.env
```

Edit `.env` file with your credentials:
```bash
# Required - Application will fail without this
ALPHA_VANTAGE_API_KEY=your_actual_api_key_here

# Required for email notifications (auto_predict.py)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=recipient@gmail.com
```

⚠️ **Security Note**: Never commit `.env` files to version control. The application will refuse to start without required environment variables.

### 3. Run the Application

```bash
cd backend
python start.py
```

The application will:
- Validate all required environment variables
- Run initial data fetch and model training (if no model exists)
- Start the FastAPI server on `http://localhost:8000`
- Provide manual endpoints for pipeline operations

**First Run**: The app automatically fetches data and trains the model on startup if no existing model is found.

## API Endpoints

### Health & Status
- `GET /` - API home page
- `GET /health` - Health check
- `GET /status` - Detailed application status

### Predictions
- `POST /predict/` - Make a stock prediction

### Manual Operations
- `POST /pipeline/run` - Run complete pipeline manually
- `POST /data/fetch` - Fetch new data manually
- `POST /model/train` - Train model manually

## Usage Examples

### Making a Prediction

```bash
curl -X POST "http://localhost:8000/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "Daily_Change": 2.5,
    "Volatility": 3.2,
    "MA_5": 150.0,
    "MA_10": 148.5,
    "MA_20": 145.0,
    "Momentum": 5.0,
    "Volume_Change": 0.1,
    "RSI_14": 65.0
  }'
**Input Validation**: All fields have validation ranges:
- `Daily_Change`: -50% to +50%
- `Volatility`: 0% to 100%
- `MA_5`, `MA_10`, `MA_20`: Must be positive
- `Momentum`: -1000 to +1000
- `Volume_Change`: -1000% to +1000%
- `RSI_14`: 0 to 100```

**Success Response (200)**:
```json
{
  "prediction": "Higher",
  "confidence": "78.5%",
  "timestamp": "2024-01-15T10:30:00",
  "features_used": ["Daily Change %", "Volatility", "MA_5", ...]
}
```

**Error Responses**:
- `422`: Invalid input data (out of range values)
- `503`: Model not loaded (run `/pipeline/run` first)
- `500`: Unexpected prediction error

### Running Pipeline Manually

```bash
curl -X POST "http://localhost:8000/pipeline/run" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "INDUSINDBK.BSE"}'
```

## Configuration

**Environment Variables** (`.env` file):
- `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key (required)
- `EMAIL_SENDER`: Gmail address for notifications (optional)
- `EMAIL_PASSWORD`: Gmail app password (optional)
- `EMAIL_RECEIVER`: Recipient email (optional)

**Code Configuration** (`backend/config.py`):
- **Supported Symbols**: Add/modify stock symbols
- **Feature Engineering**: Customize technical indicators
- **Model Parameters**: Adjust XGBoost settings
- **File Paths**: Configure data storage locations

**Security Features**:
- ✅ No hardcoded secrets in code
- ✅ Environment validation on startup
- ✅ Input sanitization and validation
- ✅ Proper error handling with appropriate HTTP codes

## Deployment Options

### Local Development
```bash
python start.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

**Using docker-compose (Recommended)**:
```bash
cd backend
# Set environment variables
echo "ALPHA_VANTAGE_API_KEY=your_key_here" > .env
docker-compose up -d
```

**Manual Docker Build**:
```bash
cd backend
docker build -t stock-prediction-api .
docker run -p 8000:8000 --env-file .env stock-prediction-api
```

**Health Check**: Docker includes automatic health monitoring via `/health` endpoint.

### Cloud Deployment

#### Heroku
1. Create `Procfile`:
   ```
   web: python start.py
   ```
2. Deploy to Heroku

#### Railway/Render
- Connect your GitHub repository
- Set environment variables
- Deploy automatically

## Monitoring

The application includes built-in monitoring:

- **Health Checks**: `/health` endpoint
- **Status Monitoring**: `/status` endpoint
- **Automatic Logging**: All operations are logged
- **Error Handling**: Comprehensive error handling

## Troubleshooting

### Common Issues

1. **Environment Variables Missing**: 
   - Error: "Missing required environment variables: ALPHA_VANTAGE_API_KEY"
   - Solution: Create `.env` file with required variables

2. **API Key Issues**: 
   - Error: "API Error" or "API Rate Limit"
   - Solution: Check API key validity and rate limits
   - The app automatically retries with exponential backoff

3. **Model Not Loading**: 
   - Error: HTTP 503 "Model not loaded"
   - Solution: Run `POST /pipeline/run` to train the model

4. **Input Validation Errors**: 
   - Error: HTTP 422 "Invalid input data"
   - Solution: Check input ranges (RSI 0-100, positive MAs, etc.)

5. **Data Fetch Failures**: 
   - Automatic retry mechanism with exponential backoff
   - Check API limits and internet connection
   - Monitor logs for specific error details

### Logs

Check the console output for detailed logs about:
- Data fetching status
- Model training progress
- API request handling
- Scheduled task execution

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │  Data Manager   │    │   External APIs │
│                 │    │                 │    │                 │
│  - REST API     │◄──►│  - Data Fetch   │◄──►│  - Alpha Vantage│
│  - Validation   │    │  - Preprocess   │    │  - Retry Logic  │
│  - Error Handle │    │  - Model Train  │    │  - Rate Limits  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │    │   Data Storage  │    │  Environment    │
│  - Status Codes │    │  - CSV Files    │    │  - Env Variables│
│  - JSON Schema  │    │  - Model Cache  │    │  - Validation   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Key Improvements**:
- 🔐 **Security**: Environment-based secrets, input validation
- 🛡️ **Reliability**: API retries, timeout handling, proper error codes
- 📊 **Monitoring**: Health checks, structured error responses
- 🔄 **Resilience**: Graceful degradation, automatic retry mechanisms

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 
