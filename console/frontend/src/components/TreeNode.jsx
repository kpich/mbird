function TreeNode({ node, onAddChild, level = 0 }) {
  const handleAddChild = () => {
    const newChildId = `node_${Date.now()}`
    onAddChild(node.id, newChildId)
  }

  return (
    <div className="tree-node-container" style={{ marginLeft: `${level * 30}px` }}>
      <div className={`tree-node ${node.is_stale ? 'tree-node-stale' : ''}`}>
        <span className="tree-node-id">
          {node.id}
        </span>
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
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default TreeNode
