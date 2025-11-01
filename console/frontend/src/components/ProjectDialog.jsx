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
      <div className="dialog-overlay">
        <div className="dialog-box">
          <h2 className="dialog-title">mbird Console</h2>
          <p>Create a new project or load an existing one.</p>

          <div className="dialog-button-group">
            <button
              onClick={() => setMode('create')}
              className="btn-primary"
            >
              Create New Project
            </button>

            <button
              onClick={() => setMode('load')}
              className="btn-secondary"
            >
              Load Existing Project
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="dialog-overlay">
      <div className="dialog-box-large">
        <div className="dialog-header">
          <h2>
            {mode === 'create' ? 'Create New Project' : 'Load Existing Project'}
          </h2>
          <button
            onClick={() => setMode(null)}
            disabled={loading}
            className="btn-back"
          >
            Back
          </button>
        </div>

        {error && (
          <div className="dialog-error">
            {error}
          </div>
        )}

        {loading ? (
          <div className="dialog-loading">Loading...</div>
        ) : (
          <DirectoryBrowser mode={mode} onSelect={handleSelectPath} />
        )}
      </div>
    </div>
  )
}

export default ProjectDialog
