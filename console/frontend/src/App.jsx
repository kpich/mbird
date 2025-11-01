import { useState } from 'react'
import ProjectDialog from './components/ProjectDialog'
import TreeView from './components/TreeView'

function App() {
  const [projectLoaded, setProjectLoaded] = useState(false)
  const [projectPath, setProjectPath] = useState(null)
  const [treeData, setTreeData] = useState(null)
  const [lastSaved, setLastSaved] = useState(null)
  const [saving, setSaving] = useState(false)

  const handleProjectLoaded = (path, tree) => {
    setProjectPath(path)
    setTreeData(tree)
    setProjectLoaded(true)
  }

  const handleTreeChange = async (newTreeData) => {
    setTreeData(newTreeData)

    await fetch('/api/tree', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTreeData),
    }).catch(err => console.error('Failed to update tree:', err))
  }

  const handleSave = async () => {
    setSaving(true)
    try {
      const response = await fetch('/api/save', { method: 'POST' })
      if (response.ok) {
        const data = await response.json()
        setLastSaved(new Date(data.timestamp))
      } else {
        console.error('Save failed:', await response.text())
      }
    } catch (err) {
      console.error('Save error:', err)
    } finally {
      setSaving(false)
    }
  }

  if (!projectLoaded) {
    return <ProjectDialog onProjectLoaded={handleProjectLoaded} />
  }

  const basename = projectPath ? projectPath.split('/').pop() : 'Unknown'

  return (
    <div className="app-container">
      <div className="app-header">
        <h2 className="app-title">{basename}</h2>
        <div className="app-header-actions">
          {lastSaved && (
            <span className="app-last-saved">
              Last saved: {lastSaved.toLocaleString()}
            </span>
          )}
          <button
            onClick={handleSave}
            disabled={saving}
            className="app-save-btn"
          >
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
      <div className="app-content">
        <TreeView treeData={treeData} onTreeChange={handleTreeChange} />
      </div>
    </div>
  )
}

export default App
