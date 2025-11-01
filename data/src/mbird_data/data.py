from pathlib import Path

from mbird_data.constants import TREE_FNAME
from mbird_data.tree import MbirdTree


class MbirdData:
    def __init__(self):
        self.tree: MbirdTree | None = None

    def load(self, dir_path: str | Path) -> None:
        """
        Load mbird data from a .mbird directory.

        Args:
            dir_path: Path to the .mbird directory
        """
        dir_path = Path(dir_path)
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        if not dir_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dir_path}")

        tree_file = dir_path / TREE_FNAME
        if not tree_file.exists():
            raise FileNotFoundError(f"Tree file not found: {tree_file}")

        self.tree = MbirdTree.load(tree_file)

    def save(self, dir_path: str | Path) -> None:
        """
        Save mbird data to a .mbird directory.

        Args:
            dir_path: Path to the .mbird directory
        """
        if self.tree is None:
            raise ValueError("No tree loaded")

        dir_path = Path(dir_path)
        dir_path.mkdir(parents=True, exist_ok=True)

        tree_file = dir_path / TREE_FNAME
        self.tree.save(tree_file)
