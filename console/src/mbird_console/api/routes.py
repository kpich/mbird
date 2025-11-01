from typing import Any

from fastapi import APIRouter, HTTPException
from mbird_data import MbirdData, MbirdNode

router = APIRouter()

current_data: MbirdData | None = None


@router.post("/api/project/create")
async def create_project() -> dict[str, Any]:
    """Create new project with single root node."""
    global current_data
    root = MbirdNode(id="root")
    current_data = MbirdData(root=root)
    return {"status": "success", "tree": current_data.root.model_dump()}


@router.post("/api/project/load")
async def load_project(tree_data: dict[str, Any]) -> dict[str, Any]:
    """Load project from tree JSON data."""
    global current_data
    try:
        root = MbirdNode(**tree_data)
        current_data = MbirdData(root=root)
        return {"status": "success", "tree": current_data.root.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/api/tree")
async def get_tree() -> dict[str, Any]:
    """Get current tree data."""
    if current_data is None or current_data.root is None:
        raise HTTPException(status_code=404, detail="No project loaded")
    return current_data.root.model_dump()


@router.post("/api/tree")
async def update_tree(tree_data: dict[str, Any]) -> dict[str, Any]:
    """Update entire tree."""
    global current_data
    try:
        root = MbirdNode(**tree_data)
        current_data = MbirdData(root=root)
        return {"status": "success", "tree": current_data.root.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
