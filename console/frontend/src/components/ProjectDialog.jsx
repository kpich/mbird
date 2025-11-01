import { useState } from 'react'

function ProjectDialog({ onProjectLoaded }) {
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [path, setPath] = useState('')
  const [mode, setMode] = useState(null)

  const handleCreateNew = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const response = await fetch('/api/project/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path }),
      })

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`Failed to create project: ${response.status} ${text}`)
      }

      const data = await response.json()
      onProjectLoaded(path, data.tree)
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  const handleLoadExisting = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const response = await fetch('/api/project/load', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path }),
      })

      if (!response.ok) {
        const text = await response.text()
        throw new Error(`Failed to load project: ${response.status} ${text}`)
      }

      const data = await response.json()
      onProjectLoaded(path, data.tree)
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
        padding: '40px',
        borderRadius: '8px',
        maxWidth: '500px',
        width: '100%',
      }}>
        <h2 style={{ marginTop: 0 }}>
          {mode === 'create' ? 'Create New Project' : 'Load Existing Project'}
        </h2>

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

        <form onSubmit={mode === 'create' ? handleCreateNew : handleLoadExisting}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
              Project Path:
            </label>
            <input
              type="text"
              value={path}
              onChange={(e) => setPath(e.target.value)}
              placeholder="/path/to/project.mbird"
              required
              style={{
                width: '100%',
                padding: '8px',
                fontSize: '14px',
                border: '1px solid #ccc',
                borderRadius: '4px',
              }}
            />
            <small style={{ color: '#666', display: 'block', marginTop: '4px' }}>
              {mode === 'create'
                ? 'Will append .mbird if not present'
                : 'Must end with .mbird'}
            </small>
          </div>

          <div style={{ display: 'flex', gap: '12px' }}>
            <button
              type="button"
              onClick={() => setMode(null)}
              disabled={loading}
              style={{
                flex: 1,
                padding: '12px 24px',
                fontSize: '16px',
                cursor: loading ? 'not-allowed' : 'pointer',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
              }}
            >
              Back
            </button>

            <button
              type="submit"
              disabled={loading || !path}
              style={{
                flex: 1,
                padding: '12px 24px',
                fontSize: '16px',
                cursor: (loading || !path) ? 'not-allowed' : 'pointer',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
              }}
            >
              {loading ? 'Processing...' : mode === 'create' ? 'Create' : 'Load'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ProjectDialog
