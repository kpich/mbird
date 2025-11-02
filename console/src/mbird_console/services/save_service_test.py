from pathlib import Path

from mbird_console.services.save_service import SaveService
from mbird_console.state import State
from mbird_data import MbirdData, MbirdNode
from mbird_data.constants import TREE_FNAME


def test_save_project_writes_to_disk(tmp_path: Path):
    project_path = tmp_path / "test_project.mbird"

    root = MbirdNode(id="root", length=None)
    data = MbirdData(root=root)

    state = State()
    service = SaveService(state)

    service.save_project(data, str(project_path))

    saved_file = project_path / TREE_FNAME
    assert saved_file.exists()


def test_save_project_returns_timestamp(tmp_path: Path):
    project_path = tmp_path / "test_project.mbird"

    root = MbirdNode(id="root", length=None)
    data = MbirdData(root=root)

    state = State()
    service = SaveService(state)

    timestamp = service.save_project(data, str(project_path))

    assert timestamp is not None


def test_save_project_updates_state(tmp_path: Path):
    project_path = tmp_path / "test_project.mbird"

    root = MbirdNode(id="root", length=None)
    data = MbirdData(root=root)

    state = State()
    service = SaveService(state)

    timestamp = service.save_project(data, str(project_path))

    assert state.last_saved == timestamp


def test_get_last_saved_returns_timestamp_after_save(tmp_path: Path):
    project_path = tmp_path / "test_project.mbird"

    root = MbirdNode(id="root", length=None)
    data = MbirdData(root=root)

    state = State()
    service = SaveService(state)

    service.save_project(data, str(project_path))
    last_saved = service.get_last_saved()

    assert last_saved is not None


def test_get_last_saved_returns_none_when_not_saved():
    state = State()
    service = SaveService(state)

    last_saved = service.get_last_saved()

    assert last_saved is None
