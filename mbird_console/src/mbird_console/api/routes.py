from typing import Annotated, Any

from fastapi import APIRouter, File, UploadFile

from mbird_console.graph_loader import load_graph

router = APIRouter()

current_graph: dict[str, Any] = {
    "nodes": [],
    "edges": [],
}


@router.get("/api/graph")
async def get_graph() -> dict[str, Any]:
    """Get current graph data."""
    return current_graph


@router.post("/api/graph")
async def update_graph(graph_data: dict[str, Any]) -> dict[str, Any]:
    """Update entire graph."""
    global current_graph
    current_graph = graph_data
    return {"status": "success", "graph": current_graph}


@router.post("/api/graph/load")
async def load_graph_file(file: Annotated[UploadFile, File()]) -> dict[str, Any]:
    """Load graph from uploaded file."""
    global current_graph
    current_graph = load_graph(file.filename or "")
    return {"status": "success", "graph": current_graph}


@router.post("/api/graph/node")
async def add_node(node: dict[str, Any]) -> dict[str, Any]:
    """Add a new node to the graph."""
    current_graph["nodes"].append(node)
    return {"status": "success", "node": node}


@router.post("/api/graph/edge")
async def add_edge(edge: dict[str, Any]) -> dict[str, Any]:
    """Add a new edge to the graph."""
    current_graph["edges"].append(edge)
    return {"status": "success", "edge": edge}
