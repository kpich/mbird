function TreeNode({ node, onAddChild, onUpdateLength, level = 0 }) {
  const handleAddChild = () => {
    const newChildId = `node_${Date.now()}`
    onAddChild(node.id, newChildId)
  }

  const handleLengthChange = (e) => {
    const newLength = parseFloat(e.target.value)
    if (!isNaN(newLength) && newLength >= 0) {
      onUpdateLength(node.id, newLength)
    }
  }

  return (
    <div className="tree-node-container" style={{ marginLeft: `${level * 30}px` }}>
      <div className={`tree-node ${node.is_stale ? 'tree-node-stale' : ''}`}>
        <span className="tree-node-id">
          {node.id}
        </span>
        {node.length !== null && node.length !== undefined && (
          <input
            type="number"
            value={node.length}
            onChange={handleLengthChange}
            step="0.1"
            min="0"
            className="tree-node-length-input"
            title="Length in seconds"
          />
        )}
        {node.length !== null && node.length !== undefined && (
          <span className="tree-node-length-display">s</span>
        )}
        <button
          onClick={handleAddChild}
          className="tree-node-add-button"
          title="Add child node"
        >
          +
        </button>
      </div>

      {node.children && node.children.length > 0 && (
        <div>
          {node.children.map((child) => (
            <TreeNode
              key={child.id}
              node={child}
              onAddChild={onAddChild}
              onUpdateLength={onUpdateLength}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default TreeNode
