function TreeNode({ node, onAddChild, level = 0 }) {
  const handleAddChild = () => {
    const newChildId = `node_${Date.now()}`
    onAddChild(node.id, newChildId)
  }

  return (
    <div style={{ marginLeft: `${level * 30}px`, marginTop: '8px' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        padding: '8px',
        border: '1px solid #ccc',
        borderRadius: '4px',
        backgroundColor: '#f9f9f9',
        width: 'fit-content',
      }}>
        <span style={{ fontFamily: 'monospace', fontWeight: 'bold' }}>
          {node.id}
        </span>
        <button
          onClick={handleAddChild}
          style={{
            width: '24px',
            height: '24px',
            borderRadius: '50%',
            border: '1px solid #007bff',
            backgroundColor: '#007bff',
            color: 'white',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '16px',
            padding: 0,
          }}
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
