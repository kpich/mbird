from pathlib import Path


def _get_config_dir() -> Path:
    """Get config directory path."""
    return Path.home() / ".mbird"


def _get_last_directory_file() -> Path:
    """Get last directory file path."""
    return _get_config_dir() / "last_directory"


def get_last_directory() -> str:
    """Get the last used directory, or home directory if none saved."""
    last_dir_file = _get_last_directory_file()
    if last_dir_file.exists():
        return last_dir_file.read_text().strip()
    return str(Path.home())


def save_last_directory(path: str) -> None:
    """Save the last used directory path."""
    config_dir = _get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    last_dir_file = _get_last_directory_file()
    last_dir_file.write_text(path)
