from pathlib import Path

import pytest

from mbird_console import config


def test_get_last_directory_returns_home_when_no_file_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    test_home = tmp_path / "fake_home"
    test_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: test_home)

    test_config_dir = tmp_path / ".mbird"
    result = config.get_last_directory(config_dir=test_config_dir)

    assert result == str(test_home)


def test_save_last_directory_creates_config_dir_and_writes_path(tmp_path: Path):
    test_path = "/some/test/path"
    test_config_dir = tmp_path / ".mbird"

    config.save_last_directory(test_path, config_dir=test_config_dir)

    last_dir_file = test_config_dir / "last_directory"

    assert test_config_dir.exists()
    assert last_dir_file.exists()
    assert last_dir_file.read_text() == test_path


def test_get_last_directory_returns_saved_path(tmp_path: Path):
    test_path = tmp_path / "saved" / "directory" / "path"
    test_path.mkdir(parents=True)
    test_config_dir = tmp_path / ".mbird"

    config.save_last_directory(str(test_path), config_dir=test_config_dir)
    result = config.get_last_directory(config_dir=test_config_dir)

    assert result == str(test_path)


def test_save_last_directory_overwrites_previous_value(tmp_path: Path):
    first_path = tmp_path / "first" / "path"
    second_path = tmp_path / "second" / "path"
    first_path.mkdir(parents=True)
    second_path.mkdir(parents=True)
    test_config_dir = tmp_path / ".mbird"

    config.save_last_directory(str(first_path), config_dir=test_config_dir)
    config.save_last_directory(str(second_path), config_dir=test_config_dir)

    result = config.get_last_directory(config_dir=test_config_dir)

    assert result == str(second_path)


def test_get_last_directory_without_config_dir_uses_home():
    """Test that passing None uses default home directory."""
    result = config.get_last_directory()
    assert isinstance(result, str)
    assert len(result) > 0


def test_save_and_get_roundtrip_with_temp_config(tmp_path: Path):
    """Test full save/get cycle with temp config directory."""
    test_config_dir = tmp_path / ".mbird"
    test_path = tmp_path / "my_project.mbird"
    test_path.mkdir()

    config.save_last_directory(str(test_path), config_dir=test_config_dir)
    result = config.get_last_directory(config_dir=test_config_dir)

    assert result == str(test_path)
    assert (test_config_dir / "last_directory").exists()


def test_get_last_directory_falls_back_to_home_when_cached_path_deleted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Test that deleted cached path falls back to home directory."""
    test_home = tmp_path / "fake_home"
    test_home.mkdir()
    monkeypatch.setattr(Path, "home", lambda: test_home)

    test_config_dir = tmp_path / ".mbird"
    test_path = tmp_path / "deleted_project.mbird"
    test_path.mkdir()

    # Save path while it exists
    config.save_last_directory(str(test_path), config_dir=test_config_dir)

    # Delete the path
    test_path.rmdir()

    # Should fall back to home
    result = config.get_last_directory(config_dir=test_config_dir)
    assert result == str(test_home)
