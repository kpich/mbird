import TreeNode from './TreeNode'

function TreeView({ treeData, onTreeChange }) {
  const addChildToNode = (parentId, newChildId) => {
    const newChild = {
      id: newChildId,
      children: [],
      is_stale: true,
      length: 10.0,
    }

    const updatedTree = addChildRecursive(treeData, parentId, newChild)
    onTreeChange(updatedTree)
  }

  const addChildRecursive = (node, parentId, newChild) => {
    if (node.id === parentId) {
      return {
        ...node,
        children: [...node.children, newChild],
      }
    }

    if (node.children && node.children.length > 0) {
      return {
        ...node,
        children: node.children.map(child => addChildRecursive(child, parentId, newChild)),
      }
    }

    return node
  }

  const updateNodeLength = (nodeId, newLength) => {
    const updatedTree = updateLengthRecursive(treeData, nodeId, newLength)
    onTreeChange(updatedTree)
  }

  const updateLengthRecursive = (node, nodeId, newLength) => {
    if (node.id === nodeId) {
      return {
        ...node,
        length: newLength,
      }
    }

    if (node.children && node.children.length > 0) {
      return {
        ...node,
        children: node.children.map(child => updateLengthRecursive(child, nodeId, newLength)),
      }
    }

    return node
  }

  if (!treeData) {
    return <div>No tree data</div>
  }

  return (
    <div className="tree-view">
      <TreeNode
        node={treeData}
        onAddChild={addChildToNode}
        onUpdateLength={updateNodeLength}
        level={0}
      />
    </div>
  )
}

export default TreeView
