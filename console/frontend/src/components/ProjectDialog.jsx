import { useState } from 'react'
import DirectoryBrowser from './DirectoryBrowser'

function ProjectDialog({ onProjectLoaded }) {
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState(null)

  const handleSelectPath = async (selectedPath) => {
    setError(null)
    setLoading(true)

    try {
      const endpoint = mode === 'create' ? '/api/project/create' : '/api/project/load'
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: selectedPath }),
      })

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`Failed to ${mode} project: ${response.status} ${text}`)
      }

      const data = await response.json()
      onProjectLoaded(selectedPath, data.tree)
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  if (!mode) {
    return (
      <div style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
      }}>
        <div style={{
          backgroundColor: 'white',
          padding: '40px',
          borderRadius: '8px',
          maxWidth: '400px',
          width: '100%',
        }}>
          <h2 style={{ marginTop: 0 }}>mbird Console</h2>
          <p>Create a new project or load an existing one.</p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <button
              onClick={() => setMode('create')}
              style={{
                padding: '12px 24px',
                fontSize: '16px',
                cursor: 'pointer',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
              }}
            >
              Create New Project
            </button>

            <button
              onClick={() => setMode('load')}
              style={{
                padding: '12px 24px',
                fontSize: '16px',
                cursor: 'pointer',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
              }}
            >
              Load Existing Project
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '30px',
        borderRadius: '8px',
        maxWidth: '600px',
        width: '100%',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2 style={{ margin: 0 }}>
            {mode === 'create' ? 'Create New Project' : 'Load Existing Project'}
          </h2>
          <button
            onClick={() => setMode(null)}
            disabled={loading}
            style={{
              padding: '8px 16px',
              fontSize: '14px',
              cursor: loading ? 'not-allowed' : 'pointer',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
            }}
          >
            Back
          </button>
        </div>

        {error && (
          <div style={{
            padding: '12px',
            marginBottom: '20px',
            backgroundColor: '#fee',
            border: '1px solid #fcc',
            borderRadius: '4px',
            color: '#c00',
          }}>
            {error}
          </div>
        )}

        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
        ) : (
          <DirectoryBrowser mode={mode} onSelect={handleSelectPath} />
        )}
      </div>
    </div>
  )
}

export default ProjectDialog
