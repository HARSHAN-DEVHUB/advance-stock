import { useState, useEffect } from 'react'
import APIService from '../services/api.js'
import { Database, TrendingUp, TrendingDown } from 'lucide-react'

function StockData() {
  const [symbol, setSymbol] = useState('INDUSINDBK.BSE')
  const [data, setData] = useState(null)
  const [processedData, setProcessedData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [dataType, setDataType] = useState('latest')
  const [rowsToShow, setRowsToShow] = useState(10)

  const supportedSymbols = [
    'INDUSINDBK.BSE',
    'RELIANCE.BSE',
    'TCS.BSE',
    'HDFCBANK.BSE',
    'INFY.BSE'
  ]

  const fetchData = async (type) => {
    setLoading(true)
    setError(null)
    setData(null)
    setProcessedData(null)

    try {
      if (type === 'latest') {
        const result = await APIService.getLatestData(symbol)
        // normalize to { rows, data }
        setData({ rows: result.data_points || 0, data: result.latest_3_days || [] })
      } else {
        const result = await APIService.getProcessedData(symbol)
        setProcessedData({ rows: result.data_points || 0, data: result.latest_3_days_processed || [] })
      }
    } catch (err) {
      setError(err.message || `Failed to fetch ${type} data`)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData(dataType)
  }, [symbol, dataType])

  const handleRefresh = () => fetchData(dataType)

  const toggleShowAll = () => setRowsToShow(prev => (prev === -1 ? 10 : -1))

  const downloadCSV = (tableData = [], filename = 'data.csv') => {
    if (!tableData || tableData.length === 0) return
    const keys = Object.keys(tableData[0])
    const csv = [keys.join(',')].concat(tableData.map(row => keys.map(k => {
      const v = row[k]
      if (v === null || v === undefined) return ''
      return typeof v === 'string' && v.includes(',') ? `"${v.replace(/"/g, '""')}"` : `${v}`
    }).join(','))).join('\n')

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }

  const renderTable = (tableData, columns) => {
    if (!tableData || tableData.length === 0) {
      return <p>No data available — try running Fetch/Preprocess in Train Model.</p>
    }

    const sliceData = rowsToShow === -1 ? tableData : tableData.slice(0, rowsToShow)

    return (
      <div className="table-container">
        <table>
          <thead>
            <tr>
              {columns.map(col => (
                <th key={col.key}>{col.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sliceData.map((row, idx) => (
              <tr key={idx}>
                {columns.map(col => (
                  <td key={col.key}>
                    {(() => {
                      const val = row[col.key]
                      const n = Number(val)
                      return Number.isFinite(n) ? n.toFixed(4) : val
                    })()}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div className="stock-data">
      <h2>Stock Data Viewer</h2>
      <p className="subtitle">View raw and processed stock market data</p>

      <div className="controls">
        <div className="form-group">
          <label>Select Symbol</label>
          <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
            {supportedSymbols.map((sym) => (
              <option key={sym} value={sym}>{sym}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Data Type</label>
          <select value={dataType} onChange={(e) => setDataType(e.target.value)}>
            <option value="latest">Latest (Raw)</option>
            <option value="processed">Processed (Features)</option>
          </select>
        </div>
      </div>

      {loading && (
        <div className="loading">
          <Database size={32} className="spinning" />
          <p>Loading data...</p>
        </div>
      )}

      {error && (
        <div className="alert alert-error">
          <p>Error: {error}</p>
        </div>
      )}

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px' }}>
        <button className="btn" onClick={handleRefresh} disabled={loading}>Refresh</button>
      </div>

      {data && dataType === 'latest' && (
        <div className="data-section">
          <h3>Latest Stock Data</h3>
          <p>Showing last 10 records from {data.rows} total rows</p>
          {renderTable(data.data, [
            { key: 'date', label: 'Date' },
            { key: 'open', label: 'Open' },
            { key: 'high', label: 'High' },
            { key: 'low', label: 'Low' },
            { key: 'close', label: 'Close' },
            { key: 'volume', label: 'Volume' }
          ])}
        </div>
      )}

      {processedData && dataType === 'processed' && (
        <div className="data-section">
          <h3>Processed Stock Data with Features</h3>
          <p>Showing last 10 records from {processedData.rows} total rows</p>
          <div style={{ display: 'flex', gap: '8px', marginBottom: '8px', justifyContent: 'flex-end' }}>
            <button className="btn small" onClick={() => downloadCSV(processedData.data, `${symbol}_processed.csv`)} disabled={!processedData.data || processedData.data.length===0}>Download CSV</button>
          </div>
          {renderTable(
            processedData.data,
            [
              { key: 'date', label: 'Date' },
              { key: 'close', label: 'Close' },
              { key: 'daily_change_percent', label: 'Daily Change %' },
              { key: 'volatility', label: 'Volatility' },
              { key: 'momentum', label: 'Momentum' },
              { key: 'volume_change', label: 'Volume_Change' },
              { key: 'ma_5', label: 'MA_5' },
              { key: 'ma_10', label: 'MA_10' },
              { key: 'ma_20', label: 'MA_20' },
              { key: 'rsi_14', label: 'RSI_14' }
            ]
          )}
        </div>
      )}
    </div>
  )
}

export default StockData
