import { useState, useEffect } from 'react'
import APIService from '../services/api.js'
import { TrendingUp, TrendingDown, Activity, Database, RefreshCw } from 'lucide-react'

function Dashboard() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    fetchStatus()
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    try {
      setRefreshing(true)
      const data = await APIService.getStatus()
      setStatus(data)
    } catch (error) {
      console.error('Error fetching status:', error)
      setStatus({ error: error.message })
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading dashboard...</div>
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Dashboard Overview</h2>
        <button 
          onClick={fetchStatus} 
          disabled={refreshing}
          className="btn btn-secondary"
        >
          <RefreshCw size={18} className={refreshing ? 'spinning' : ''} />
          {refreshing ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <h3>Model Status</h3>
            <p className={`status-${status?.model_loaded ? 'active' : 'inactive'}`}>
              {status?.model_loaded ? '✅ Loaded' : '❌ Not Loaded'}
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Database size={24} />
          </div>
          <div className="stat-content">
            <h3>Scaler Status</h3>
            <p className={`status-${status?.scaler_loaded ? 'active' : 'inactive'}`}>
              {status?.scaler_loaded ? '✅ Loaded' : '❌ Not Loaded'}
            </p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <h3>Default Symbol</h3>
            <p>{status?.default_symbol || 'N/A'}</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <h3>Last Update</h3>
            <p>{status?.last_update ? new Date(status.last_update).toLocaleDateString() : 'Never'}</p>
          </div>
        </div>
      </div>

      <div className="info-section">
        <h3>Supported Symbols</h3>
        <div className="symbol-list">
          {status?.supported_symbols?.map((symbol) => (
            <span key={symbol} className="symbol-badge">{symbol}</span>
          ))}
        </div>
      </div>

      {status?.note && (
        <div className="alert alert-info">
          <p>ℹ️ {status.note}</p>
        </div>
      )}

      {status?.error && (
        <div className="alert alert-error">
          <p>❌ Error: {status.error}</p>
        </div>
      )}

      <div className="info-section">
        <h3>API Configuration</h3>
        <div className="config-grid">
          <div className="config-item">
            <label>API Status:</label>
            <span className="badge badge-success">{status?.api_status || 'running'}</span>
          </div>
          <div className="config-item">
            <label>Manual Mode:</label>
            <span className="badge badge-info">Yes</span>
          </div>
          <div className="config-item">
            <label>Scheduler:</label>
            <span className="badge badge-warning">Disabled</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
