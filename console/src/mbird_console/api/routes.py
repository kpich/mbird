from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from mbird_data import MbirdData, MbirdNode

router = APIRouter()

current_data: MbirdData | None = None
current_path: str | None = None
last_saved: datetime | None = None


@router.post("/api/project/create")
async def create_project(request: dict[str, Any]) -> dict[str, Any]:
    """Create new project with single root node."""
    global current_data, current_path

    dir_path = request.get("path")
    if not dir_path:
        raise HTTPException(status_code=400, detail="Missing 'path' in request")

    root = MbirdNode(id="root")
    current_data = MbirdData(root=root)
    current_path = dir_path

    return {"status": "success", "tree": current_data.root.model_dump()}


@router.post("/api/project/load")
async def load_project(request: dict[str, Any]) -> dict[str, Any]:
    """Load project from directory path."""
    global current_data, current_path

    dir_path = request.get("path")
    if not dir_path:
        raise HTTPException(status_code=400, detail="Missing 'path' in request")

    try:
        current_data = MbirdData.load(dir_path)
        current_path = dir_path
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


@router.post("/api/save")
async def save_project() -> dict[str, Any]:
    """Save project to disk using MbirdData.save()."""
    global current_data, current_path, last_saved

    if current_data is None or current_data.root is None:
        raise HTTPException(status_code=404, detail="No project loaded")

    if current_path is None:
        raise HTTPException(status_code=400, detail="No project path set")

    try:
        current_data.save(current_path)
        last_saved = datetime.now(timezone.utc)

        return {
            "status": "success",
            "timestamp": last_saved.isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/api/save/status")
async def get_save_status() -> dict[str, Any]:
    """Get last saved timestamp."""
    return {
        "last_saved": last_saved.isoformat() if last_saved else None,
    }
