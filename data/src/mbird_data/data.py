import json
from pathlib import Path

from mbird_data.constants import TREE_FNAME
from mbird_data.models import MbirdNode


class MbirdData:
    def __init__(self):
        self.root: MbirdNode | None = None

    def load(self, dir_path: str | Path) -> None:
        """
        Load mbird data from a directory.

        Args:
            dir_path: Path to the directory
        """
        dir_path = Path(dir_path)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")

        tree_file = dir_path / TREE_FNAME
        if not tree_file.exists():
            raise FileNotFoundError(f"Tree file not found: {tree_file}")

        data = json.loads(tree_file.read_text())
        self.root = MbirdNode(**data)

    def save(self, dir_path: str | Path) -> None:
        """
        Save mbird data to a directory.

        Args:
            dir_path: Path to the directory
        """
        if self.root is None:
            raise ValueError("No root node loaded")

        dir_path = Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)

        tree_file = dir_path / TREE_FNAME
        tree_file.write_text(json.dumps(self.root.model_dump(), indent=2))
