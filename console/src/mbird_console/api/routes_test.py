from pathlib import Path

from fastapi.testclient import TestClient
from mbird_data.constants import TREE_FNAME
import pytest

from mbird_console.api import routes
from mbird_console.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    """Reset global state before each test."""
    routes.current_data = None
    routes.current_path = None
    routes.last_saved = None
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
    invalid_tree = {"children": []}

    update_response = client.post("/api/tree", json=invalid_tree)
    assert update_response.status_code == 400


def test_browse_directory_lists_only_directories(tmp_path: Path):
    (tmp_path / "subdir1").mkdir()
    (tmp_path / "subdir2").mkdir()
    (tmp_path / "file.txt").write_text("content")

    browse_response = client.get(f"/api/filesystem/browse?path={tmp_path}")
    assert browse_response.status_code == 200

    data = browse_response.json()
    assert len(data["directories"]) == 2
    assert any(d["name"] == "subdir1" for d in data["directories"])
    assert any(d["name"] == "subdir2" for d in data["directories"])


def test_browse_directory_filters_hidden_directories(tmp_path: Path):
    (tmp_path / ".hidden").mkdir()
    (tmp_path / "visible").mkdir()

    browse_response = client.get(f"/api/filesystem/browse?path={tmp_path}")
    assert browse_response.status_code == 200

    data = browse_response.json()
    assert len(data["directories"]) == 1
    assert data["directories"][0]["name"] == "visible"


def test_browse_nonexistent_directory_raises_error():
    browse_response = client.get("/api/filesystem/browse?path=/nonexistent/path")
    assert browse_response.status_code == 404
    assert "not found" in browse_response.json()["detail"].lower()


def test_browse_file_instead_of_directory_raises_error(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("content")

    browse_response = client.get(f"/api/filesystem/browse?path={file_path}")
    assert browse_response.status_code == 400
    assert "Not a directory" in browse_response.json()["detail"]


def test_browse_returns_parent_path(tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    browse_response = client.get(f"/api/filesystem/browse?path={subdir}")
    assert browse_response.status_code == 200

    data = browse_response.json()
    assert data["parent"] == str(tmp_path)


def test_get_home_directory_returns_valid_path():
    home_response = client.get("/api/filesystem/home")
    assert home_response.status_code == 200

    data = home_response.json()
    assert "path" in data
    assert len(data["path"]) > 0
    assert Path(data["path"]).exists()
