import { useState, useEffect } from 'react'

function DirectoryBrowser({ mode, onSelect }) {
  const [currentPath, setCurrentPath] = useState(null)
  const [directories, setDirectories] = useState([])
  const [parentPath, setParentPath] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [newDirName, setNewDirName] = useState('')

  useEffect(() => {
    // Load default directory on mount (last used or home)
    fetch('/api/filesystem/default')
      .then(res => res.json())
      .then(data => {
        loadDirectory(data.path)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  const loadDirectory = async (path) => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`/api/filesystem/browse?path=${encodeURIComponent(path)}`)
      if (!response.ok) {
        throw new Error('Failed to load directory')
      }
      const data = await response.json()
      setCurrentPath(data.current)
      setDirectories(data.directories)
      setParentPath(data.parent)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectCurrent = () => {
    if (mode === 'create' && newDirName) {
      const fullPath = `${currentPath}/${newDirName}`
      onSelect(fullPath)
    } else {
      onSelect(currentPath)
    }
  }

  const handleSelectDirectory = (dirPath) => {
    if (mode === 'load') {
      // For load, navigate into the directory
      loadDirectory(dirPath)
    } else {
      // For create, select this directory and allow entering new name
      loadDirectory(dirPath)
    }
  }

  if (loading) {
    return <div style={{ padding: '20px' }}>Loading...</div>
  }

  if (error) {
    return <div style={{ padding: '20px', color: 'red' }}>Error: {error}</div>
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '400px' }}>
      <div style={{
        padding: '12px',
        backgroundColor: '#f0f0f0',
        borderBottom: '1px solid #ccc',
        fontFamily: 'monospace',
        fontSize: '13px',
      }}>
        {currentPath}
      </div>

      {parentPath && (
        <button
          onClick={() => loadDirectory(parentPath)}
          style={{
            padding: '8px 12px',
            textAlign: 'left',
            border: 'none',
            borderBottom: '1px solid #eee',
            backgroundColor: 'white',
            cursor: 'pointer',
          }}
        >
          ⬆ ..
        </button>
      )}

      <div style={{
        flex: 1,
        overflowY: 'auto',
        border: '1px solid #ccc',
      }}>
        {directories.length === 0 ? (
          <div style={{ padding: '12px', color: '#666' }}>No directories</div>
        ) : (
          directories.map(dir => (
            <button
              key={dir.path}
              onClick={() => handleSelectDirectory(dir.path)}
              style={{
                width: '100%',
                padding: '8px 12px',
                textAlign: 'left',
                border: 'none',
                borderBottom: '1px solid #eee',
                backgroundColor: 'white',
                cursor: 'pointer',
              }}
              onMouseEnter={(e) => e.target.style.backgroundColor = '#f5f5f5'}
              onMouseLeave={(e) => e.target.style.backgroundColor = 'white'}
            >
              📁 {dir.name}
            </button>
          ))
        )}
      </div>

      {mode === 'create' && (
        <div style={{ padding: '12px', borderTop: '1px solid #ccc' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>
            New directory name:
          </label>
          <input
            type="text"
            value={newDirName}
            onChange={(e) => setNewDirName(e.target.value)}
            placeholder="my-project"
            style={{
              width: '100%',
              padding: '8px',
              border: '1px solid #ccc',
              borderRadius: '4px',
            }}
          />
        </div>
      )}

      <div style={{ padding: '12px', borderTop: '1px solid #ccc', backgroundColor: '#f9f9f9' }}>
        <button
          onClick={handleSelectCurrent}
          disabled={mode === 'create' && !newDirName}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: (mode === 'create' && !newDirName) ? 'not-allowed' : 'pointer',
          }}
        >
          {mode === 'create' ? 'Create Here' : 'Select This Directory'}
        </button>
      </div>
    </div>
  )
}

export default DirectoryBrowser
