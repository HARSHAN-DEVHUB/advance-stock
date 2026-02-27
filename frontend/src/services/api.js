/**
 * API Service Layer
 * Centralized API calls for the Stock Prediction Frontend
 */

const API_BASE = '/api'

class APIService {
  /**
   * Health & Status Endpoints
   */
  
  static async getHealth() {
    const response = await fetch(`${API_BASE}/health`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  static async getStatus() {
    const response = await fetch(`${API_BASE}/status`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  /**
   * Data Endpoints
   */

  static async fetchData(symbol = 'INDUSINDBK.BSE') {
    const response = await fetch(`${API_BASE}/data/fetch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol }),
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  static async getLatestData(symbol = 'INDUSINDBK.BSE') {
    const response = await fetch(`${API_BASE}/data/latest?symbol=${symbol}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  static async getProcessedData(symbol = 'INDUSINDBK.BSE') {
    const response = await fetch(`${API_BASE}/data/processed?symbol=${symbol}`)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  static async preprocessData(symbol = 'INDUSINDBK.BSE') {
    const response = await fetch(`${API_BASE}/preprocess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol }),
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  /**
   * Model Training Endpoints
   */

  static async runPipeline(symbol = 'INDUSINDBK.BSE') {
    const response = await fetch(`${API_BASE}/pipeline/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol }),
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  static async trainModel(symbol = 'INDUSINDBK.BSE') {
    const response = await fetch(`${API_BASE}/model/train`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol }),
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }

  /**
   * Prediction Endpoint
   */

  static async predict(data) {
    const response = await fetch(`${API_BASE}/predict/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return response.json()
  }
}

export default APIService
