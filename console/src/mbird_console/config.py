from pathlib import Path

CONFIG_DIR = Path.home() / ".mbird"
LAST_DIRECTORY_FILE = CONFIG_DIR / "last_directory"


def get_last_directory() -> str:
    """Get the last used directory, or home directory if none saved."""
    if LAST_DIRECTORY_FILE.exists():
        return LAST_DIRECTORY_FILE.read_text().strip()
    return str(Path.home())


def save_last_directory(path: str) -> None:
    """Save the last used directory path."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    LAST_DIRECTORY_FILE.write_text(path)
