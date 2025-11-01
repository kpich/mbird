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
    <div style={{ width: '100%', height: '100%', display: 'flex', flexDirection: 'column' }}>
      <div style={{
        padding: '16px',
        borderBottom: '1px solid #ccc',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        backgroundColor: '#f9f9f9',
      }}>
        <h2 style={{ margin: 0 }}>{basename}</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {lastSaved && (
            <span style={{ fontSize: '14px', color: '#666' }}>
              Last saved: {lastSaved.toLocaleString()}
            </span>
          )}
          <button
            onClick={handleSave}
            disabled={saving}
            style={{
              padding: '8px 16px',
              fontSize: '14px',
              cursor: saving ? 'not-allowed' : 'pointer',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
            }}
          >
            {saving ? 'Saving...' : 'Save'}
          </button>
        </div>
      </div>
      <div style={{ flex: 1, overflow: 'auto' }}>
        <TreeView treeData={treeData} onTreeChange={handleTreeChange} />
      </div>
    </div>
  )
}

export default App
