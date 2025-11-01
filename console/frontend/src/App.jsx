import { useState } from 'react'
import ProjectDialog from './components/ProjectDialog'
import GraphEditor from './components/GraphEditor'

const TREE_FILENAME = 'tree.json'

function App() {
  const [projectLoaded, setProjectLoaded] = useState(false)
  const [dirHandle, setDirHandle] = useState(null)
  const [treeData, setTreeData] = useState(null)

  const handleProjectLoaded = (handle, tree) => {
    setDirHandle(handle)
    setTreeData(tree)
    setProjectLoaded(true)
  }

  const handleTreeChange = async (newTreeData) => {
    setTreeData(newTreeData)

    // Save to backend
    await fetch('/api/tree', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newTreeData),
    }).catch(err => console.error('Failed to update tree:', err))

    // Save to file
    if (dirHandle) {
      try {
        const fileHandle = await dirHandle.getFileHandle(TREE_FILENAME, { create: true })
        const writable = await fileHandle.createWritable()
        await writable.write(JSON.stringify(newTreeData, null, 2))
        await writable.close()
      } catch (err) {
        console.error('Failed to save tree.json:', err)
      }
    }
  }

  if (!projectLoaded) {
    return <ProjectDialog onProjectLoaded={handleProjectLoaded} />
  }

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <div style={{ padding: '20px' }}>
        <h3>Project loaded: {treeData?.id}</h3>
        <pre>{JSON.stringify(treeData, null, 2)}</pre>
        {/* TODO: Convert tree to graph and show GraphEditor */}
      </div>
    </div>
  )
}

export default App
