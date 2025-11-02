from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
import pytest

from mbird_console.api import routes
from mbird_console.main import app
from mbird_data.constants import TREE_FNAME

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test."""
    routes.state.reset()

    # Clean up real config file to prevent test pollution
    real_config_file = Path.home() / ".mbird" / "last_directory"
    if real_config_file.exists():
        real_config_file.unlink()

    yield

    # Clean up again after test
    if real_config_file.exists():
        real_config_file.unlink()


def test_save_writes_to_disk_using_mbird_data_save(tmp_path: Path):
    project_path = str(tmp_path / "test_project.mbird")

    create_response = client.post("/api/project/create", json={"path": project_path})
    assert create_response.status_code == 200

    save_response = client.post("/api/save")
    assert save_response.status_code == 200

    data = save_response.json()
    assert data["status"] == "success"
    assert "timestamp" in data

    saved_file = Path(project_path) / TREE_FNAME
    assert saved_file.exists()


def test_save_status_returns_timestamp_after_save(tmp_path: Path):
    project_path = str(tmp_path / "test_project.mbird")

    client.post("/api/project/create", json={"path": project_path})
    client.post("/api/save")

    status_response = client.get("/api/save/status")
    assert status_response.status_code == 200

    data = status_response.json()
    assert data["last_saved"] is not None


def test_save_without_project_raises_error():
    save_response = client.post("/api/save")
    assert save_response.status_code == 404
    assert "No project loaded" in save_response.json()["detail"]


def test_load_reads_from_disk_using_mbird_data_load(tmp_path: Path):
    project_path = str(tmp_path / "existing.mbird")

    client.post("/api/project/create", json={"path": project_path})
    client.post("/api/save")

    load_response = client.post("/api/project/load", json={"path": project_path})
    assert load_response.status_code == 200

    data = load_response.json()
    assert data["status"] == "success"
    assert data["tree"]["id"] == "root"


def test_create_project_returns_root_node():
    create_response = client.post(
        "/api/project/create", json={"path": "/tmp/test.mbird"}
    )
    assert create_response.status_code == 200

    data = create_response.json()
    assert data["status"] == "success"
    assert data["tree"]["id"] == "root"
    assert data["tree"]["children"] == []


def test_create_project_without_path_raises_error():
    create_response = client.post("/api/project/create", json={})
    assert create_response.status_code == 400
    assert "Missing 'path'" in create_response.json()["detail"]


def test_create_project_sets_current_path():
    client.post("/api/project/create", json={"path": "/tmp/test.mbird"})

    tree_response = client.get("/api/tree")
    assert tree_response.status_code == 200
    assert tree_response.json()["id"] == "root"


def test_get_tree_when_no_project_loaded_raises_error():
    tree_response = client.get("/api/tree")
    assert tree_response.status_code == 404
    assert "No project loaded" in tree_response.json()["detail"]


def test_get_tree_returns_current_tree():
    client.post("/api/project/create", json={"path": "/tmp/test.mbird"})

    tree_response = client.get("/api/tree")
    assert tree_response.status_code == 200

    data = tree_response.json()
    assert data["id"] == "root"
    assert data["children"] == []


def test_update_tree_with_valid_data_succeeds():
    client.post("/api/project/create", json={"path": "/tmp/test.mbird"})

    new_tree = {
        "id": "root",
        "length": None,
        "children": [
            {"id": "child1", "length": 10.0, "children": []},
            {"id": "child2", "length": 5.0, "children": []},
        ],
    }

    update_response = client.post("/api/tree", json=new_tree)
    assert update_response.status_code == 200

    data = update_response.json()
    assert data["status"] == "success"
    assert len(data["tree"]["children"]) == 2
    assert data["tree"]["children"][0]["id"] == "child1"

    tree_response = client.get("/api/tree")
    assert len(tree_response.json()["children"]) == 2


def test_update_tree_with_cyclic_data_raises_error():
    cyclic_tree = {
        "id": "node1",
        "length": None,
        "children": [
            {
                "id": "node2",
                "length": None,
                "children": [{"id": "node1", "length": 10.0, "children": []}],
            }
        ],
    }

    update_response = client.post("/api/tree", json=cyclic_tree)
    assert update_response.status_code == 400
    assert "Cycle detected" in update_response.json()["detail"]


def test_update_tree_with_invalid_structure_raises_error():
    invalid_tree: dict[str, Any] = {"children": [], "length": None}

    update_response = client.post("/api/tree", json=invalid_tree)
    assert update_response.status_code == 400


def test_regenerate_sets_is_stale_false_for_all_nodes(tmp_path: Path):
    project_path = str(tmp_path / "test_project.mbird")

    client.post("/api/project/create", json={"path": project_path})

    tree_response = client.get("/api/tree")
    tree_data = tree_response.json()
    assert tree_data["is_stale"] is True

    regenerate_response = client.post("/api/regenerate")
    assert regenerate_response.status_code == 200

    data = regenerate_response.json()
    assert data["status"] == "success"
    assert data["tree"]["is_stale"] is False


def test_regenerate_without_project_raises_error():
    regenerate_response = client.post("/api/regenerate")
    assert regenerate_response.status_code == 404
    assert "No project loaded" in regenerate_response.json()["detail"]


def test_adding_child_transfers_parent_length_to_child():
    client.post("/api/project/create", json={"path": "/tmp/test.mbird"})

    tree_with_new_child = {
        "id": "root",
        "length": 15.0,
        "children": [{"id": "new_child", "length": 10.0, "children": []}],
    }

    update_response = client.post("/api/tree", json=tree_with_new_child)
    assert update_response.status_code == 200

    data = update_response.json()
    assert data["tree"]["length"] is None
    assert data["tree"]["children"][0]["length"] == 15.0


def test_regenerate_creates_audio_files_for_stale_leaf_nodes(tmp_path: Path):
    """Integration test: regenerate creates audio files through full stack."""
    project_path = str(tmp_path / "test_project.mbird")

    # Create project with stale leaf nodes
    client.post("/api/project/create", json={"path": project_path})

    # Add children
    tree_with_children = {
        "id": "root",
        "length": None,
        "children": [
            {"id": "child1", "length": 2.0, "children": []},
            {"id": "child2", "length": 1.5, "children": []},
        ],
    }
    client.post("/api/tree", json=tree_with_children)

    # Regenerate should create audio files
    regenerate_response = client.post("/api/regenerate")
    assert regenerate_response.status_code == 200

    # Check audio files were created
    clips_dir = Path(project_path) / "clips"
    assert clips_dir.exists()
    assert (clips_dir / "child1.wav").exists()
    assert (clips_dir / "child2.wav").exists()

    # Check sound_file was set in response
    data = regenerate_response.json()
    assert data["tree"]["children"][0]["sound_file"] == "child1.wav"
    assert data["tree"]["children"][1]["sound_file"] == "child2.wav"
