# Stock Prediction API

A FastAPI-based application that predicts stock opening prices using machine learning. The application automatically fetches data, preprocesses it, trains models, and provides predictions via REST API.

## Features

- 🤖 **Automatic Data Fetching**: Fetches stock data from Alpha Vantage API
- 🔧 **Data Preprocessing**: Cleans and prepares data with technical indicators
- 🎯 **ML Model Training**: Uses XGBoost for prediction
- ⏰ **Scheduled Updates**: Automatically updates data and retrains models
- 🌐 **REST API**: Easy-to-use endpoints for predictions
- 📊 **Health Monitoring**: Built-in health checks and status endpoints

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Copy `env_example.txt` to `.env` and add your Alpha Vantage API key:

```bash
cp env_example.txt .env
# Edit .env and add your API key
```

### 3. Run the Application

```bash
python start.py
```

The application will:
- Run initial data fetch and model training (if no model exists)
- Start the FastAPI server on `http://localhost:8000`
- Begin scheduled tasks for automatic updates

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
```

Response:
```json
{
  "prediction": "Higher",
  "confidence": "78.5%",
  "timestamp": "2024-01-15T10:30:00",
  "features_used": ["Daily Change %", "Volatility", "MA_5", ...]
}
```

### Running Pipeline Manually

```bash
curl -X POST "http://localhost:8000/pipeline/run" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "INDUSINDBK.BSE"}'
```

## Configuration

Edit `config.py` to customize:

- **Supported Symbols**: Add more stock symbols
- **Update Intervals**: Change how often data updates and model retrains
- **API Settings**: Modify Alpha Vantage API configuration

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
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "start.py"]
```

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

1. **API Key Issues**: Ensure your Alpha Vantage API key is valid
2. **Model Not Loading**: Run `/pipeline/run` to train the model
3. **Data Fetch Failures**: Check API limits and internet connection
4. **Port Conflicts**: Change port in `start.py` if 8000 is busy

### Logs

Check the console output for detailed logs about:
- Data fetching status
- Model training progress
- API request handling
- Scheduled task execution

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │  Data Manager   │    │  Scheduler      │
│                 │    │                 │    │                 │
│  - REST API     │◄──►│  - Data Fetch   │◄──►│  - Auto Updates │
│  - Predictions  │    │  - Preprocess   │    │  - Model Retrain│
│  - Health Check │    │  - Model Train  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   HTTP Client   │    │   Data Files    │    │  Background     │
│  (Postman/etc)  │    │  (CSV, PKL)     │    │   Tasks        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 
