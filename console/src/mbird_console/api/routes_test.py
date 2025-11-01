from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
from mbird_data.constants import TREE_FNAME
import pytest

from mbird_console import config
from mbird_console.api import routes
from mbird_console.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Reset global state and isolate config to temp directory."""
    routes.current_data = None
    routes.current_path = None
    routes.last_saved = None

    test_config_dir = tmp_path / ".mbird"

    monkeypatch.setattr(config, "_get_config_dir", lambda: test_config_dir)
    monkeypatch.setattr(
        config, "_get_last_directory_file", lambda: test_config_dir / "last_directory"
    )

    yield


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
        "children": [
            {"id": "child1", "children": []},
            {"id": "child2", "children": []},
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
        "children": [
            {
                "id": "node2",
                "children": [{"id": "node1", "children": []}],
            }
        ],
    }

    update_response = client.post("/api/tree", json=cyclic_tree)
    assert update_response.status_code == 400
    assert "Cycle detected" in update_response.json()["detail"]


def test_update_tree_with_invalid_structure_raises_error():
    invalid_tree: dict[str, Any] = {"children": []}

    update_response = client.post("/api/tree", json=invalid_tree)
    assert update_response.status_code == 400


def test_default_directory_returns_home_when_no_saved_directory():
    default_response = client.get("/api/filesystem/default")
    assert default_response.status_code == 200

    data = default_response.json()
    home_response = client.get("/api/filesystem/home")
    home_data = home_response.json()

    assert data["path"] == home_data["path"]


def test_default_directory_returns_last_directory_after_creating_project(
    tmp_path: Path,
):
    project_path = str(tmp_path / "test_project.mbird")

    client.post("/api/project/create", json={"path": project_path})

    default_response = client.get("/api/filesystem/default")
    assert default_response.status_code == 200

    data = default_response.json()
    assert data["path"] == project_path


def test_default_directory_persists_after_loading_project(tmp_path: Path):
    project_path = str(tmp_path / "loaded_project.mbird")

    client.post("/api/project/create", json={"path": project_path})
    client.post("/api/save")

    routes.current_data = None
    routes.current_path = None

    client.post("/api/project/load", json={"path": project_path})

    default_response = client.get("/api/filesystem/default")
    assert default_response.status_code == 200

    data = default_response.json()
    assert data["path"] == project_path


def test_default_directory_updates_when_opening_different_project(tmp_path: Path):
    project_a = str(tmp_path / "project_a.mbird")
    project_b = str(tmp_path / "project_b.mbird")

    client.post("/api/project/create", json={"path": project_a})

    default_response = client.get("/api/filesystem/default")
    assert default_response.json()["path"] == project_a

    client.post("/api/project/create", json={"path": project_b})

    default_response = client.get("/api/filesystem/default")
    assert default_response.json()["path"] == project_b
