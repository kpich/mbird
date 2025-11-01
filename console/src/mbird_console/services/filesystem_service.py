from pathlib import Path
from typing import Any


class FilesystemService:
    """Manages filesystem operations and directory tracking."""

    def __init__(self, last_run_pointer_dir: Path | None = None):
        """Initialize with optional dir for last_directory file (for testing)."""
        self.last_run_pointer_dir = (
            last_run_pointer_dir
            if last_run_pointer_dir is not None
            else Path.home() / ".mbird"
        )

    def get_home_directory(self) -> str:
        """Get user's home directory."""
        return str(Path.home())

    def get_default_directory(self) -> str:
        """Get default directory for file browser (last used or home)."""
        return self.get_last_directory()

    def get_last_directory(self) -> str:
        """Get the last used directory, or home directory if none saved."""
        last_dir_file = self.last_run_pointer_dir / "last_directory"
        if last_dir_file.exists():
            cached_path = last_dir_file.read_text().strip()
            if Path(cached_path).exists():
                return cached_path
        return str(Path.home())

    def save_last_directory(self, path: str) -> None:
        """Save the last used directory path."""
        self.last_run_pointer_dir.mkdir(parents=True, exist_ok=True)
        last_dir_file = self.last_run_pointer_dir / "last_directory"
        last_dir_file.write_text(path)

    def browse_directory(self, path: str = "/") -> dict[str, Any]:
        """
        List directories in the given path.

        Returns list of directories (not files) that user can navigate to.
        """
        dir_path = Path(path).expanduser().resolve()

        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        directories = []
        try:
            for entry in sorted(dir_path.iterdir()):
                if entry.is_dir() and not entry.name.startswith("."):
                    directories.append({"name": entry.name, "path": str(entry)})
        except PermissionError:
            pass

        parent = str(dir_path.parent) if dir_path.parent != dir_path else None

        return {"current": str(dir_path), "parent": parent, "directories": directories}
