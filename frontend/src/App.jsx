import { useState, useEffect } from 'react'
import { TrendingUp, Activity, Database, Zap } from 'lucide-react'
import APIService from './services/api.js'
import Dashboard from './components/Dashboard.jsx'
import PredictForm from './components/PredictForm.jsx'
import TrainModel from './components/TrainModel.jsx'
import StockData from './components/StockData.jsx'
import './styles/App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [apiStatus, setApiStatus] = useState({ status: 'checking' })

  useEffect(() => {
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    try {
      const data = await APIService.getHealth()
      setApiStatus(data)
    } catch (error) {
      setApiStatus({ status: 'offline', error: error.message })
    }
  }

  const tabs = [
    { id: 'dashboard', name: 'Dashboard', icon: Activity },
    { id: 'predict', name: 'Predict', icon: TrendingUp },
    { id: 'train', name: 'Train Model', icon: Zap },
    { id: 'data', name: 'Stock Data', icon: Database },
  ]

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <TrendingUp size={32} />
            <h1>Stock Prediction</h1>
          </div>
          <div className={`api-status ${apiStatus.status}`}>
            <span className="status-dot"></span>
            API: {apiStatus.status}
          </div>
        </div>
      </header>

      <nav className="app-nav">
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              className={`nav-button ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <Icon size={20} />
              <span>{tab.name}</span>
            </button>
          )
        })}
      </nav>

      <main className="app-main">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'predict' && <PredictForm />}
        {activeTab === 'train' && <TrainModel />}
        {activeTab === 'data' && <StockData />}
      </main>

      <footer className="app-footer">
        <p>© 2026 Stock Prediction API - Built By HARSHAN </p>
      </footer>
    </div>
  )
}

export default App
