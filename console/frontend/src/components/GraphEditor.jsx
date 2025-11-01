import { useCallback, useState } from 'react'
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow'
import 'reactflow/dist/style.css'

function GraphEditor({ initialNodes, initialEdges, onGraphChange }) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges)

  const onConnect = useCallback((params) => {
    const newEdges = addEdge(params, edges)
    setEdges(newEdges)
    onGraphChange({ nodes, edges: newEdges })
  }, [edges, nodes, onGraphChange, setEdges])

  const handleNodesChange = useCallback((changes) => {
    onNodesChange(changes)
  }, [onNodesChange])

  const handleEdgesChange = useCallback((changes) => {
    onEdgesChange(changes)
  }, [onEdgesChange])

  return (
    <div className="graph-editor">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        onConnect={onConnect}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  )
}

export default GraphEditor
