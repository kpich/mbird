from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from mbird_console.services import (
    FilesystemService,
    ProjectService,
    SaveService,
    TreeService,
)
from mbird_console.state import State

router = APIRouter()

state = State()
project_service = ProjectService(state)
tree_service = TreeService()
save_service = SaveService(state)
filesystem_service = FilesystemService()


@router.post("/api/project/create")
async def create_project(request: dict[str, Any]) -> dict[str, Any]:
    """Create new project with single root node."""
    dir_path = request.get("path")
    if not dir_path:
        raise HTTPException(status_code=400, detail="Missing 'path' in request")

    data = project_service.create_project(dir_path)
    filesystem_service.save_last_directory(dir_path)

    if data.root is None:
        raise HTTPException(status_code=500, detail="Failed to create project")
    return {"status": "success", "tree": data.root.model_dump()}


@router.post("/api/project/load")
async def load_project(request: dict[str, Any]) -> dict[str, Any]:
    """Load project from directory path."""
    dir_path = request.get("path")
    if not dir_path:
        raise HTTPException(status_code=400, detail="Missing 'path' in request")

    try:
        data = project_service.load_project(dir_path)
        filesystem_service.save_last_directory(dir_path)

        if data.root is None:
            raise HTTPException(status_code=500, detail="Failed to load project")
        return {"status": "success", "tree": data.root.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/api/tree")
async def get_tree() -> dict[str, Any]:
    """Get current tree data."""
    data = project_service.get_current_data()
    if data is None or data.root is None:
        raise HTTPException(status_code=404, detail="No project loaded")
    return data.root.model_dump()


@router.post("/api/tree")
async def update_tree(tree_data: dict[str, Any]) -> dict[str, Any]:
    """Update entire tree."""
    try:
        # Preserve directory from existing data
        existing_directory = (
            state.current_data.directory if state.current_data else None
        )
        data = tree_service.update_tree(tree_data)
        data.directory = existing_directory
        state.current_data = data

        if data.root is None:
            raise HTTPException(status_code=500, detail="Failed to update tree")
        return {"status": "success", "tree": data.root.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/api/regenerate")
async def regenerate() -> dict[str, Any]:
    """Run generate() to set is_stale=False for all nodes."""
    data = project_service.get_current_data()
    if data is None or data.root is None:
        raise HTTPException(status_code=404, detail="No project loaded")

    tree_service.regenerate(data)
    return {"status": "success", "tree": data.root.model_dump()}


@router.post("/api/save")
async def save_project() -> dict[str, Any]:
    """Save project to disk using MbirdData.save()."""
    data = project_service.get_current_data()
    path = project_service.get_current_path()

    if data is None or data.root is None:
        raise HTTPException(status_code=404, detail="No project loaded")
    if path is None:
        raise HTTPException(status_code=400, detail="No project path set")

    try:
        timestamp = save_service.save_project(data, path)
        return {"status": "success", "timestamp": timestamp.isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/api/save/status")
async def get_save_status() -> dict[str, Any]:
    """Get last saved timestamp."""
    last_saved = save_service.get_last_saved()
    return {"last_saved": last_saved.isoformat() if last_saved else None}


@router.get("/api/filesystem/home")
async def get_home_directory() -> dict[str, Any]:
    """Get user's home directory."""
    return {"path": filesystem_service.get_home_directory()}


@router.get("/api/filesystem/default")
async def get_default_directory() -> dict[str, Any]:
    """Get default directory for file browser (last used or home)."""
    return {"path": filesystem_service.get_default_directory()}


@router.get("/api/filesystem/browse")
async def browse_directory(path: str = "/") -> dict[str, Any]:
    """
    List directories in the given path.

    Returns list of directories (not files) that user can navigate to.
    """
    try:
        return filesystem_service.browse_directory(path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail="Directory not found") from e
    except NotADirectoryError as e:
        raise HTTPException(status_code=400, detail="Not a directory") from e


@router.get("/api/play")
async def play_concatenated_audio() -> FileResponse:
    """Serve the concatenated audio file (cur.wav) for playback."""
    data = project_service.get_current_data()
    if data is None or data.directory is None:
        raise HTTPException(status_code=404, detail="No project loaded")

    audio_path = data.directory / "cur.wav"
    if not audio_path.exists():
        raise HTTPException(
            status_code=404, detail="No audio file available. Try regenerating first."
        )

    return FileResponse(
        path=str(audio_path), media_type="audio/wav", filename="cur.wav"
    )
