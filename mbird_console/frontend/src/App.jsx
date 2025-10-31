import { useState, useEffect } from 'react'
import GraphEditor from './components/GraphEditor'

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/graph')
      .then(res => res.json())
      .then(data => {
        setGraphData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load graph:', err)
        setLoading(false)
      })
  }, [])

  const handleGraphChange = (newGraphData) => {
    setGraphData(newGraphData)
    fetch('/api/graph', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newGraphData),
    }).catch(err => console.error('Failed to save graph:', err))
  }

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading...</div>
  }

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <GraphEditor
        initialNodes={graphData.nodes}
        initialEdges={graphData.edges}
        onGraphChange={handleGraphChange}
      />
    </div>
  )
}

export default App
