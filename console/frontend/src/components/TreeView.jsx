import TreeNode from './TreeNode'

function TreeView({ treeData, onTreeChange }) {
  const addChildToNode = (parentId, newChildId) => {
    const newChild = {
      id: newChildId,
      children: [],
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

  if (!treeData) {
    return <div>No tree data</div>
  }

  return (
    <div className="tree-view">
      <TreeNode
        node={treeData}
        onAddChild={addChildToNode}
        level={0}
      />
    </div>
  )
}

export default TreeView
