import { useState } from 'react'
import APIService from '../services/api.js'
import { Zap, Play, Loader, CheckCircle, XCircle, Database, Settings } from 'lucide-react'

function TrainModel() {
  const [symbol, setSymbol] = useState('INDUSINDBK.BSE')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [activeOperation, setActiveOperation] = useState(null)

  const supportedSymbols = [
    'INDUSINDBK.BSE',
    'RELIANCE.BSE',
    'TCS.BSE',
    'HDFCBANK.BSE',
    'INFY.BSE'
  ]

  const handleOperation = async (operation) => {
    setLoading(true)
    setError(null)
    setResult(null)
    setActiveOperation(operation)

    try {
      let data
      switch(operation) {
        case 'pipeline':
          data = await APIService.runPipeline(symbol)
          break
        case 'fetch':
          data = await APIService.fetchData(symbol)
          break
        case 'preprocess':
          data = await APIService.preprocessData(symbol)
          break
        case 'train':
          data = await APIService.trainModel(symbol)
          break
        case 'latest':
          data = await APIService.getLatestData(symbol)
          break
        case 'processed':
          data = await APIService.getProcessedData(symbol)
          break
        default:
          throw new Error('Unknown operation')
      }
      setResult({ ...data, type: operation })
    } catch (err) {
      setError(err.message || `Failed to ${operation}`)
    } finally {
      setLoading(false)
      setActiveOperation(null)
    }
  }

  const operations = [
    {
      id: 'pipeline',
      title: 'Full Pipeline',
      description: 'Fetch data, preprocess, and train model in one step',
      icon: Zap,
      variant: 'primary'
    },
    {
      id: 'fetch',
      title: 'Fetch Data',
      description: 'Download latest stock data from Alpha Vantage',
      icon: Play,
      variant: 'secondary'
    },
    {
      id: 'preprocess',
      title: 'Preprocess Data',
      description: 'Calculate technical indicators (MA, RSI, momentum)',
      icon: Settings,
      variant: 'secondary'
    },
    {
      id: 'train',
      title: 'Train Model',
      description: 'Train the XGBoost model with existing data',
      icon: Zap,
      variant: 'secondary'
    },
    {
      id: 'latest',
      title: 'Load Latest Data',
      description: 'Load raw stock data into memory',
      icon: Database,
      variant: 'secondary'
    },
    {
      id: 'processed',
      title: 'Load Processed Data',
      description: 'Load data with calculated features',
      icon: Database,
      variant: 'secondary'
    }
  ]

  return (
    <div className="train-model">
      <h2>Model Training & Data Operations</h2>
      <p className="subtitle">Manage your stock prediction pipeline</p>

      <div className="form-group">
        <label>Select Stock Symbol</label>
        <select
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          disabled={loading}
        >
          {supportedSymbols.map((sym) => (
            <option key={sym} value={sym}>{sym}</option>
          ))}
        </select>
      </div>

      <div className="action-grid">
        {operations.map((op) => {
          const Icon = op.icon
          return (
            <div key={op.id} className="action-card">
              <Icon size={32} />
              <h3>{op.title}</h3>
              <p>{op.description}</p>
              <button
                onClick={() => handleOperation(op.id)}
                disabled={loading}
                className={`btn btn-${op.variant}`}
              >
                {loading && activeOperation === op.id ? (
                  <>
                    <Loader size={20} className="spinning" />
                    {op.id === 'pipeline' ? 'Running...' : 
                     op.id === 'fetch' ? 'Fetching...' :
                     op.id === 'preprocess' ? 'Processing...' :
                     op.id === 'train' ? 'Training...' :
                     'Loading...'}
                  </>
                ) : (
                  <>
                    <Play size={20} />
                    {op.id === 'fetch' ? 'Fetch Data' :
                     op.id === 'preprocess' ? 'Preprocess' :
                     op.id === 'train' ? 'Train Model' :
                     op.id === 'pipeline' ? 'Run Pipeline' :
                     op.id === 'latest' ? 'Load Data' :
                     'Load Processed'}
                  </>
                )}
              </button>
            </div>
          )
        })}
      </div>

      {error && (
        <div className="alert alert-error">
          <XCircle size={20} />
          <div>
            <h4>Error</h4>
            <p>{error}</p>
          </div>
        </div>
      )}

      {result && (
        <div className="alert alert-success">
          <CheckCircle size={20} />
          <div>
            <h4>✅ {result.message || `${result.type} completed successfully`}</h4>
            {result.rows && <p>📊 Rows processed: {result.rows}</p>}
            {result.timestamp && <p>🕐 Completed at: {new Date(result.timestamp).toLocaleString()}</p>}
            {result.symbol && <p>📈 Symbol: {result.symbol}</p>}
            {result.data && <p>📁 Data records: {Array.isArray(result.data) ? result.data.length : 'Loaded'}</p>}
          </div>
        </div>
      )}

      <div className="info-section">
        <h3>📋 Operation Guide</h3>
        <div className="guide-grid">
          <div className="guide-item">
            <h4>🔄 Full Pipeline</h4>
            <p>Complete workflow: downloads data → preprocesses → trains model. <strong>Start here first!</strong></p>
          </div>
          <div className="guide-item">
            <h4>📥 Fetch Data</h4>
            <p>Downloads raw OHLCV data from Alpha Vantage. Required before preprocessing.</p>
          </div>
          <div className="guide-item">
            <h4>🔧 Preprocess Data</h4>
            <p>Calculates technical indicators (moving averages, RSI, momentum). Requires fetched data.</p>
          </div>
          <div className="guide-item">
            <h4>🧠 Train Model</h4>
            <p>Trains XGBoost classifier on preprocessed data. Requires preprocessed data.</p>
          </div>
          <div className="guide-item">
            <h4>📂 Load Latest Data</h4>
            <p>Loads raw stock data. Useful for viewing OHLCV values.</p>
          </div>
          <div className="guide-item">
            <h4>📊 Load Processed Data</h4>
            <p>Loads data with features calculated. Useful for viewing indicators.</p>
          </div>
        </div>
      </div>

      <div className="info-section warning">
        <h3>⚠️ Important Notes</h3>
        <ul>
          <li><strong>Always run "Full Pipeline" first</strong> to setup everything</li>
          <li>Operations must be done in order: Fetch → Preprocess → Train</li>
          <li>You can skip steps by running "Full Pipeline" which does all three</li>
          <li>Use "Load Latest Data" and "Load Processed Data" only to view data</li>
          <li>Model training requires sufficient data (at least 60-100 samples)</li>
        </ul>
      </div>
    </div>
  )
}

export default TrainModel
