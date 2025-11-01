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
    test_path = "/saved/directory/path"
    test_config_dir = tmp_path / ".mbird"

    config.save_last_directory(test_path, config_dir=test_config_dir)
    result = config.get_last_directory(config_dir=test_config_dir)

    assert result == test_path


def test_save_last_directory_overwrites_previous_value(tmp_path: Path):
    first_path = "/first/path"
    second_path = "/second/path"
    test_config_dir = tmp_path / ".mbird"

    config.save_last_directory(first_path, config_dir=test_config_dir)
    config.save_last_directory(second_path, config_dir=test_config_dir)

    result = config.get_last_directory(config_dir=test_config_dir)

    assert result == second_path
