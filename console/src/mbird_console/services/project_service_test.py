from pathlib import Path

from mbird_console.services.project_service import ProjectService
from mbird_console.state import State


def test_create_project_returns_root_node():
    state = State()
    service = ProjectService(state)

    data = service.create_project("/tmp/test.mbird")

    assert data.root is not None
    assert data.root.id == "root"
    assert data.root.children == []


def test_create_project_sets_current_state():
    state = State()
    service = ProjectService(state)

    data = service.create_project("/tmp/test.mbird")

    assert state.current_data == data
    assert state.current_path == "/tmp/test.mbird"


def test_load_project_reads_from_disk(tmp_path: Path):
    project_path = tmp_path / "existing.mbird"

    state = State()
    service = ProjectService(state)

    service.create_project(str(project_path))
    created_data = state.current_data
    assert created_data is not None
    created_data.save(str(project_path))

    state.reset()

    loaded_data = service.load_project(str(project_path))

    assert loaded_data.root is not None
    assert loaded_data.root.id == "root"


def test_load_project_sets_current_state(tmp_path: Path):
    project_path = tmp_path / "existing.mbird"

    state = State()
    service = ProjectService(state)

    service.create_project(str(project_path))
    assert state.current_data is not None
    state.current_data.save(str(project_path))

    state.reset()

    loaded_data = service.load_project(str(project_path))

    assert state.current_data == loaded_data
    assert state.current_path == str(project_path)


def test_get_current_data_returns_loaded_data():
    state = State()
    service = ProjectService(state)

    service.create_project("/tmp/test.mbird")

    data = service.get_current_data()
    assert data is not None
    assert data.root is not None
    assert data.root.id == "root"


def test_get_current_path_returns_project_path():
    state = State()
    service = ProjectService(state)

    service.create_project("/tmp/test.mbird")

    path = service.get_current_path()
    assert path == "/tmp/test.mbird"


def test_has_project_returns_true_when_project_loaded():
    state = State()
    service = ProjectService(state)

    assert service.has_project() is False

    service.create_project("/tmp/test.mbird")

    assert service.has_project() is True


def test_has_project_returns_false_when_no_project():
    state = State()
    service = ProjectService(state)

    assert service.has_project() is False
