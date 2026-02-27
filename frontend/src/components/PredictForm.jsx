import { useState } from 'react'
import APIService from '../services/api.js'
import { TrendingUp, TrendingDown, Loader } from 'lucide-react'

function PredictForm() {
  const [formData, setFormData] = useState({
    Daily_Change: 0,
    Volatility: 0,
    MA_5: 100,
    MA_10: 100,
    MA_20: 100,
    Momentum: 0,
    Volume_Change: 0,
    RSI_14: 50,
  })
  
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || 0
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const result = await APIService.predict(formData)
      setPrediction(result)
    } catch (err) {
      setError(err.message || 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="predict-form">
      <h2>Stock Price Prediction</h2>
      <p className="subtitle">Enter technical indicators to predict the next opening price direction</p>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="form-group">
            <label>Daily Change (%)</label>
            <input
              type="number"
              name="Daily_Change"
              value={formData.Daily_Change}
              onChange={handleChange}
              step="0.1"
              min="-50"
              max="50"
              required
            />
            <small>Range: -50% to +50%</small>
          </div>

          <div className="form-group">
            <label>Volatility (%)</label>
            <input
              type="number"
              name="Volatility"
              value={formData.Volatility}
              onChange={handleChange}
              step="0.1"
              min="0"
              max="100"
              required
            />
            <small>Range: 0% to 100%</small>
          </div>

          <div className="form-group">
            <label>MA 5-day</label>
            <input
              type="number"
              name="MA_5"
              value={formData.MA_5}
              onChange={handleChange}
              step="0.01"
              min="0.01"
              required
            />
            <small>Must be positive</small>
          </div>

          <div className="form-group">
            <label>MA 10-day</label>
            <input
              type="number"
              name="MA_10"
              value={formData.MA_10}
              onChange={handleChange}
              step="0.01"
              min="0.01"
              required
            />
            <small>Must be positive</small>
          </div>

          <div className="form-group">
            <label>MA 20-day</label>
            <input
              type="number"
              name="MA_20"
              value={formData.MA_20}
              onChange={handleChange}
              step="0.01"
              min="0.01"
              required
            />
            <small>Must be positive</small>
          </div>

          <div className="form-group">
            <label>Momentum</label>
            <input
              type="number"
              name="Momentum"
              value={formData.Momentum}
              onChange={handleChange}
              step="0.1"
              min="-1000"
              max="1000"
              required
            />
            <small>Range: -1000 to +1000</small>
          </div>

          <div className="form-group">
            <label>Volume Change</label>
            <input
              type="number"
              name="Volume_Change"
              value={formData.Volume_Change}
              onChange={handleChange}
              step="0.1"
              min="-10"
              max="10"
              required
            />
            <small>Range: -1000% to +1000%</small>
          </div>

          <div className="form-group">
            <label>RSI 14</label>
            <input
              type="number"
              name="RSI_14"
              value={formData.RSI_14}
              onChange={handleChange}
              step="0.1"
              min="0"
              max="100"
              required
            />
            <small>Range: 0 to 100</small>
          </div>
        </div>

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? (
            <>
              <Loader size={20} className="spinning" />
              Predicting...
            </>
          ) : (
            <>
              <TrendingUp size={20} />
              Get Prediction
            </>
          )}
        </button>
      </form>

      {error && (
        <div className="alert alert-error">
          <p>Error: {error}</p>
        </div>
      )}

      {prediction && (
        <div className={`prediction-result ${prediction.prediction?.toLowerCase()}`}>
          <div className="prediction-icon">
            {prediction.prediction === 'Higher' ? (
              <TrendingUp size={48} />
            ) : (
              <TrendingDown size={48} />
            )}
          </div>
          <h3>Prediction: {prediction.prediction}</h3>
          <p className="confidence">
            Confidence: {(prediction.confidence * 100).toFixed(2)}%
          </p>
          <p className="prediction-message">{prediction.message}</p>
        </div>
      )}
    </div>
  )
}

export default PredictForm
