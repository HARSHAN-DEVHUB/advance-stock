# Stock Prediction API

Comprehensive project repository for a production-ready FastAPI application that predicts stock opening prices using machine learning and technical analysis. This repository contains a backend FastAPI service, frontend React app, data, and tooling to fetch, preprocess, train, and serve models.

## Contents

- `backend/` - FastAPI backend, data pipeline, training and prediction scripts
- `frontend/` - React frontend for interacting with the API
- `data/` - Raw and processed CSVs and model artifacts

## Features

- Intelligent data fetching from Alpha Vantage with retries and exponential backoff
- Technical indicator preprocessing (MA, RSI, momentum, volatility)
- XGBoost model training with input validation and error handling
- Pydantic request validation and strict input ranges
- Health and status endpoints for monitoring
- Docker and docker-compose support for deployment

## Quick Start

### Prerequisites

- Python 3.9+
- Alpha Vantage API Key (register at https://www.alphavantage.co/)

### Install

```bash
pip install -r backend/requirements.txt
```

### Configure Environment

Copy and edit the environment example for required variables:

```bash
cp backend/env_example.txt backend/.env
# Edit backend/.env and set ALPHA_VANTAGE_API_KEY and optional email credentials
```

Security: never commit `.env` files; the app validates required variables at startup.

### Run (Local)

```bash
cd backend
python start.py
```

This will validate environment variables, fetch initial data, train a model if absent, and serve the API on http://localhost:8000

## Backend API Endpoints

- `GET /health` - Health check (model status)
- `GET /status` - Detailed application and model status
- `POST /predict/` - Make a prediction (validated input)
- `GET /data/latest` - Recent raw data
- `GET /data/processed` - Processed data with features
- `POST /data/fetch` - Manually fetch data
- `POST /pipeline/run` - Run full pipeline (fetch → preprocess → train)
- `POST /model/train` - Train model only

### Prediction Input (validation)

All input fields are validated by Pydantic with these ranges:

```json
{
   "Daily_Change": -50.0,    // -50% to +50%
   "Volatility": 0.0,        // 0% to 100%
   "MA_5": 1.0,              // positive
   "MA_10": 1.0,             // positive
   "MA_20": 1.0,             // positive
   "Momentum": -1000.0,      // -1000 to +1000
   "Volume_Change": -1000.0, // -1000% to +1000%
   "RSI_14": 0.0             // 0 to 100
}
```

## Usage Examples

Making a prediction:

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

Typical responses:

- `200` success with `prediction`, `confidence`, `timestamp`, `features_used`
- `422` invalid input
- `503` model not loaded (run `/pipeline/run`)
- `500` server error

Run the pipeline manually:

```bash
curl -X POST "http://localhost:8000/pipeline/run" -H "Content-Type: application/json" -d '{"symbol": "INDUSINDBK.BSE"}'
```

## Data Pipeline & Storage

Flow:
1. Fetch OHLCV data from Alpha Vantage
2. Validate and clean data
3. Preprocess to compute technical features (MA, RSI, momentum, volatility)
4. Train XGBoost classifier
5. Serve predictions via FastAPI

Storage:

- Raw data: `data/{symbol}_stock_data.csv`
- Processed data: `data/{symbol}_stock_data_processed.csv`
- Model: `data/stock_prediction_model.pkl`
- Scaler: `data/scaler.pkl`

Scripts (backend):

- `python predict.py` - standalone prediction helper
- `python train_model.py [symbol]` - train model
- `python data_fetch.py [symbol]` - fetch raw data
- `python preprocess.py [symbol]` - preprocess raw data
- `python test_api.py` - run API integration tests

## Reliability & Error Handling

- Automatic retries with exponential backoff for external API calls
- 30-second timeouts for external requests
- Rate limit handling and clear error messages
- Data quality checks before processing

HTTP error mapping:

- `404` data not found
- `422` validation error
- `503` model not loaded
- `500` unexpected error

## Deployment

Local development:

```bash
cd backend
python start.py
```

Docker (recommended for production):

```bash
cd backend
docker-compose up -d
# or manual
docker build -t stock-prediction-api .
docker run -p 8000:8000 --env-file .env stock-prediction-api
```

Cloud options:

- Heroku: create a `Procfile` with `web: python start.py` and deploy
- Railway/Render: connect repo and set environment variables
- `./deploy.sh docker` or `./deploy.sh local` (helper script included)

## Frontend

The `frontend/` folder contains a React app (Vite) with components for dashboard, prediction form, training UI, and data display. Start it with:

```bash
cd frontend
npm install
npm run dev
```

Default dev server runs on port 3001.

## Monitoring & Observability

- `/health` and `/status` endpoints
- Logging for data fetches, training, and API requests
- Graceful shutdown and startup validation

## Troubleshooting

Environment issues:

```bash
# Missing API key
echo "ALPHA_VANTAGE_API_KEY=your_key" >> backend/.env

# Validation error on startup
cp backend/env_example.txt backend/.env
# Edit with real values
```

Model issues:

```bash
# Model not found
curl -X POST http://localhost:8000/pipeline/run

# Run tests
python backend/test_api.py
```

Data quality:

- The app retries failed requests and validates datasets before training. Check logs for Alpha Vantage errors and rate limits.

## Architecture

High-level diagram:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │  Data Manager   │    │   External APIs │
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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement and test changes
4. Submit a pull request

## License

MIT License

