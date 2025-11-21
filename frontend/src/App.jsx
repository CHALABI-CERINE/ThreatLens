import { useState, useEffect } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

function App() {
  const [collectedItems, setCollectedItems] = useState([])
  const [alerts, setAlerts] = useState([])
  const [processResults, setProcessResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // Fetch collected items on mount
  useEffect(() => {
    fetchCollectedItems()
  }, [])

  const fetchCollectedItems = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/collect`)
      const data = await response.json()
      setCollectedItems(data.items || [])
    } catch (err) {
      setError('Failed to fetch collected items: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchAlerts = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_BASE_URL}/alerts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: collectedItems })
      })
      const data = await response.json()
      setAlerts(data.alerts || [])
    } catch (err) {
      setError('Failed to fetch alerts: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const processTexts = async () => {
    setLoading(true)
    setError(null)
    const sampleTexts = [
      'Critical security vulnerability detected in production system',
      'Routine maintenance scheduled for next week'
    ]
    try {
      const response = await fetch(`${API_BASE_URL}/process`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texts: sampleTexts })
      })
      const data = await response.json()
      setProcessResults(data.results)
      console.log('Process results:', data.results)
    } catch (err) {
      setError('Failed to process texts: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🔍 ThreatLens Dashboard</h1>
        <p>Cyber Threat Intelligence Monitoring</p>
      </header>

      {error && <div className="error">{error}</div>}

      <div className="container">
        <section className="section">
          <div className="section-header">
            <h2>Collected Items</h2>
            <button onClick={fetchCollectedItems} disabled={loading}>
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
          <div className="items-list">
            {collectedItems.length === 0 ? (
              <p className="empty">No items collected yet</p>
            ) : (
              collectedItems.map((item, idx) => (
                <div key={idx} className="item">
                  <div className="item-header">Item {idx + 1}</div>
                  <pre>{JSON.stringify(item, null, 2)}</pre>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>Alerts</h2>
            <button onClick={fetchAlerts} disabled={loading || collectedItems.length === 0}>
              {loading ? 'Loading...' : 'Check Alerts'}
            </button>
          </div>
          <div className="items-list">
            {alerts.length === 0 ? (
              <p className="empty">No alerts generated</p>
            ) : (
              alerts.map((alert, idx) => (
                <div key={idx} className="item alert-item">
                  <div className="item-header">Alert {idx + 1}</div>
                  <pre>{JSON.stringify(alert, null, 2)}</pre>
                </div>
              ))
            )}
          </div>
        </section>

        <section className="section">
          <div className="section-header">
            <h2>NLP Processing</h2>
            <button onClick={processTexts} disabled={loading}>
              {loading ? 'Processing...' : 'Process Sample Texts'}
            </button>
          </div>
          <div className="items-list">
            {processResults ? (
              <div className="item">
                <div className="item-header">Processing Results</div>
                <pre>{JSON.stringify(processResults, null, 2)}</pre>
              </div>
            ) : (
              <p className="empty">Click "Process Sample Texts" to run NLP analysis</p>
            )}
          </div>
        </section>
      </div>
    </div>
  )
}

export default App
