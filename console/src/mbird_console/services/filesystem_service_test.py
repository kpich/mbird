from pathlib import Path

import pytest

from mbird_console.services.filesystem_service import FilesystemService


def test_get_home_directory_returns_home():
    service = FilesystemService()
    result = service.get_home_directory()
    assert result == str(Path.home())


def test_get_last_directory_returns_home_when_no_file_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    test_home = tmp_path / "fake_home"
    test_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: test_home)

    test_last_run_pointer_dir = tmp_path / ".mbird"
    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)

    result = service.get_last_directory()
    assert result == str(test_home)


def test_save_last_directory_creates_config_dir_and_writes_path(tmp_path: Path):
    test_path = tmp_path / "some" / "test" / "path"
    test_path.mkdir(parents=True)
    test_last_run_pointer_dir = tmp_path / ".mbird"

    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)
    service.save_last_directory(str(test_path))

    last_dir_file = test_last_run_pointer_dir / "last_directory"
    assert test_last_run_pointer_dir.exists()
    assert last_dir_file.exists()
    assert last_dir_file.read_text() == str(test_path)


def test_get_last_directory_returns_saved_path(tmp_path: Path):
    test_path = tmp_path / "saved" / "directory" / "path"
    test_path.mkdir(parents=True)
    test_last_run_pointer_dir = tmp_path / ".mbird"

    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)
    service.save_last_directory(str(test_path))
    result = service.get_last_directory()

    assert result == str(test_path)


def test_save_last_directory_overwrites_previous_value(tmp_path: Path):
    first_path = tmp_path / "first" / "path"
    second_path = tmp_path / "second" / "path"
    first_path.mkdir(parents=True)
    second_path.mkdir(parents=True)
    test_last_run_pointer_dir = tmp_path / ".mbird"

    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)
    service.save_last_directory(str(first_path))
    service.save_last_directory(str(second_path))

    result = service.get_last_directory()
    assert result == str(second_path)


def test_get_default_directory_returns_last_directory(tmp_path: Path):
    test_path = tmp_path / "project" / "path"
    test_path.mkdir(parents=True)
    test_last_run_pointer_dir = tmp_path / ".mbird"

    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)
    service.save_last_directory(str(test_path))

    result = service.get_default_directory()
    assert result == str(test_path)


def test_save_and_get_roundtrip_with_temp_config(tmp_path: Path):
    test_last_run_pointer_dir = tmp_path / ".mbird"
    test_path = tmp_path / "my_project.mbird"
    test_path.mkdir()

    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)
    service.save_last_directory(str(test_path))
    result = service.get_last_directory()

    assert result == str(test_path)
    assert (test_last_run_pointer_dir / "last_directory").exists()


def test_get_last_directory_falls_back_to_home_when_cached_path_deleted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    test_home = tmp_path / "fake_home"
    test_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: test_home)

    test_last_run_pointer_dir = tmp_path / ".mbird"
    test_path = tmp_path / "deleted_project.mbird"
    test_path.mkdir()

    service = FilesystemService(last_run_pointer_dir=test_last_run_pointer_dir)
    service.save_last_directory(str(test_path))

    test_path.rmdir()

    result = service.get_last_directory()
    assert result == str(test_home)


def test_browse_directory_lists_directories(tmp_path: Path):
    subdir1 = tmp_path / "subdir1"
    subdir2 = tmp_path / "subdir2"
    subdir1.mkdir()
    subdir2.mkdir()

    (tmp_path / "file.txt").write_text("test")

    service = FilesystemService()
    result = service.browse_directory(str(tmp_path))

    assert result["current"] == str(tmp_path)
    assert len(result["directories"]) == 2
    assert result["directories"][0]["name"] == "subdir1"
    assert result["directories"][1]["name"] == "subdir2"


def test_browse_directory_raises_error_when_not_found():
    service = FilesystemService()

    with pytest.raises(FileNotFoundError):
        service.browse_directory("/nonexistent/path")


def test_browse_directory_raises_error_when_not_directory(tmp_path: Path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("test")

    service = FilesystemService()

    with pytest.raises(NotADirectoryError):
        service.browse_directory(str(file_path))


def test_browse_directory_excludes_hidden_directories(tmp_path: Path):
    visible_dir = tmp_path / "visible"
    hidden_dir = tmp_path / ".hidden"
    visible_dir.mkdir()
    hidden_dir.mkdir()

    service = FilesystemService()
    result = service.browse_directory(str(tmp_path))

    assert len(result["directories"]) == 1
    assert result["directories"][0]["name"] == "visible"


def test_browse_directory_returns_parent_path(tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    service = FilesystemService()
    result = service.browse_directory(str(subdir))

    assert result["parent"] == str(tmp_path)
