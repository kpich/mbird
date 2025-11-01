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
    return <div className="directory-browser-loading">Loading...</div>
  }

  if (error) {
    return <div className="directory-browser-error">Error: {error}</div>
  }

  return (
    <div className="directory-browser">
      <div className="directory-path-display">
        {currentPath}
      </div>

      {parentPath && (
        <button
          onClick={() => loadDirectory(parentPath)}
          className="directory-up-button"
        >
          ⬆ ..
        </button>
      )}

      <div className="directory-list">
        {directories.length === 0 ? (
          <div className="directory-empty">No directories</div>
        ) : (
          directories.map(dir => (
            <button
              key={dir.path}
              onClick={() => handleSelectDirectory(dir.path)}
              className="directory-item"
            >
              📁 {dir.name}
            </button>
          ))
        )}
      </div>

      {mode === 'create' && (
        <div className="directory-create-section">
          <label className="directory-create-label">
            New directory name:
          </label>
          <input
            type="text"
            value={newDirName}
            onChange={(e) => setNewDirName(e.target.value)}
            placeholder="my-project"
            className="directory-create-input"
          />
        </div>
      )}

      <div className="directory-select-section">
        <button
          onClick={handleSelectCurrent}
          disabled={mode === 'create' && !newDirName}
          className="directory-select-button"
        >
          {mode === 'create' ? 'Create Here' : 'Select This Directory'}
        </button>
      </div>
    </div>
  )
}

export default DirectoryBrowser
