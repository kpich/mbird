import { useState } from 'react'

const TREE_FILENAME = 'tree.json'

function ProjectDialog({ onProjectLoaded }) {
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleCreateNew = async () => {
    setError(null)
    setLoading(true)

    try {
      // Check if File System Access API is supported
      if (!window.showDirectoryPicker) {
        throw new Error('File System Access API not supported. Please use Chrome or Edge.')
      }

      // Get directory handle
      const dirHandle = await window.showDirectoryPicker({ mode: 'readwrite' })

      // Create new project on backend
      const response = await fetch('/api/project/create', { method: 'POST' })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to create project')
      }

      // Write tree.json to selected directory
      const fileHandle = await dirHandle.getFileHandle(TREE_FILENAME, { create: true })
      const writable = await fileHandle.createWritable()
      await writable.write(JSON.stringify(data.tree, null, 2))
      await writable.close()

      // Notify parent with directory handle and tree data
      onProjectLoaded(dirHandle, data.tree)
    } catch (err) {
      if (err.name === 'AbortError') {
        // User cancelled, ignore
        setLoading(false)
        return
      }
      setError(err.message)
      setLoading(false)
    }
  }

  const handleLoadExisting = async () => {
    setError(null)
    setLoading(true)

    try {
      // Check if File System Access API is supported
      if (!window.showDirectoryPicker) {
        throw new Error('File System Access API not supported. Please use Chrome or Edge.')
      }

      // Get directory handle
      const dirHandle = await window.showDirectoryPicker({ mode: 'readwrite' })

      // Read tree.json from directory
      const fileHandle = await dirHandle.getFileHandle(TREE_FILENAME)
      const file = await fileHandle.getFile()
      const contents = await file.text()
      const treeData = JSON.parse(contents)

      // Load project on backend
      const response = await fetch('/api/project/load', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(treeData),
      })
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to load project')
      }

      // Notify parent with directory handle and tree data
      onProjectLoaded(dirHandle, data.tree)
    } catch (err) {
      if (err.name === 'AbortError') {
        // User cancelled, ignore
        setLoading(false)
        return
      }
      if (err.name === 'NotFoundError') {
        setError(`tree.json not found in selected directory`)
      } else {
        setError(err.message)
      }
      setLoading(false)
    }
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
        maxWidth: '400px',
        width: '100%',
      }}>
        <h2 style={{ marginTop: 0 }}>mbird Console</h2>
        <p>Create a new project or load an existing one.</p>

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

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <button
            onClick={handleCreateNew}
            disabled={loading}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              cursor: loading ? 'not-allowed' : 'pointer',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
            }}
          >
            {loading ? 'Creating...' : 'Create New Project'}
          </button>

          <button
            onClick={handleLoadExisting}
            disabled={loading}
            style={{
              padding: '12px 24px',
              fontSize: '16px',
              cursor: loading ? 'not-allowed' : 'pointer',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
            }}
          >
            {loading ? 'Loading...' : 'Load Existing Project'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProjectDialog
