from pathlib import Path


def get_last_directory(config_dir: Path | None = None) -> str:
    """Get the last used directory, or home directory if none saved."""
    if config_dir is None:
        config_dir = Path.home() / ".mbird"

    last_dir_file = config_dir / "last_directory"
    if last_dir_file.exists():
        return last_dir_file.read_text().strip()
    return str(Path.home())


def save_last_directory(path: str, config_dir: Path | None = None) -> None:
    """Save the last used directory path."""
    if config_dir is None:
        config_dir = Path.home() / ".mbird"

    config_dir.mkdir(parents=True, exist_ok=True)
    last_dir_file = config_dir / "last_directory"
    last_dir_file.write_text(path)
