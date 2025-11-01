from pathlib import Path

from fastapi.testclient import TestClient
from mbird_data.constants import TREE_FNAME

from mbird_console.main import app

client = TestClient(app)


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
