import { useState } from 'react'
import ProjectDialog from './components/ProjectDialog'
import TreeView from './components/TreeView'

function App() {
  const [projectLoaded, setProjectLoaded] = useState(false)
  const [projectPath, setProjectPath] = useState(null)
  const [treeData, setTreeData] = useState(null)
  const [lastSaved, setLastSaved] = useState(null)
  const [saving, setSaving] = useState(false)
  const [regenerating, setRegenerating] = useState(false)
  const [playing, setPlaying] = useState(false)

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

  const handleRegenerate = async () => {
    setRegenerating(true)
    try {
      const response = await fetch('/api/regenerate', { method: 'POST' })
      if (response.ok) {
        const data = await response.json()
        setTreeData(data.tree)
      } else {
        console.error('Regenerate failed:', await response.text())
      }
    } catch (err) {
      console.error('Regenerate error:', err)
    } finally {
      setRegenerating(false)
    }
  }

  const handlePlay = async () => {
    setPlaying(true)
    try {
      const response = await fetch('/api/play')
      if (response.ok) {
        const audioBlob = await response.blob()
        const audioUrl = URL.createObjectURL(audioBlob)
        const audio = new Audio(audioUrl)

        audio.onended = () => {
          setPlaying(false)
          URL.revokeObjectURL(audioUrl)
        }

        audio.onerror = () => {
          setPlaying(false)
          URL.revokeObjectURL(audioUrl)
          console.error('Audio playback failed')
        }

        await audio.play()
      } else {
        console.error('Play failed:', await response.text())
        setPlaying(false)
      }
    } catch (err) {
      console.error('Play error:', err)
      setPlaying(false)
    }
  }

  if (!projectLoaded) {
    return <ProjectDialog onProjectLoaded={handleProjectLoaded} />
  }

  const basename = projectPath ? projectPath.split('/').pop() : 'Unknown'

  return (
    <div className="app-container">
      <div className="app-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            onClick={handleRegenerate}
            disabled={regenerating}
            className="app-regenerate-btn"
          >
            {regenerating ? 'Regenerating...' : 'Regenerate'}
          </button>
          <button
            onClick={handlePlay}
            disabled={playing}
            className="app-play-btn"
          >
            {playing ? 'Playing...' : 'Play'}
          </button>
          <h2 className="app-title">{basename}</h2>
        </div>
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
