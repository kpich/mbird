from typing import Any

from mbird_data import MbirdData, MbirdNode


class TreeService:
    """Manages tree operations and transformations."""

    @staticmethod
    def get_tree(data: MbirdData) -> dict[str, Any]:
        """Get tree data as dictionary."""
        if data.root is None:
            raise ValueError("No root node in project data")
        return data.root.model_dump()

    @staticmethod
    def update_tree(tree_data: dict[str, Any]) -> MbirdData:
        """Update tree with validation and length transfer."""
        tree_data = TreeService.transfer_length_to_leaves(tree_data)
        root = MbirdNode(**tree_data)
        return MbirdData(root=root)

    @staticmethod
    def regenerate(data: MbirdData) -> MbirdData:
        """Run generate() to set is_stale=False for all nodes."""
        if data.root is None:
            raise ValueError("No root node in project data")
        TreeService.generate(data.root)
        return data

    @staticmethod
    def generate(node: MbirdNode) -> None:
        """Recursively set is_stale=False for all nodes in tree."""
        node.is_stale = False
        for child in node.children:
            TreeService.generate(child)

    @staticmethod
    def transfer_length_to_leaves(tree_data: dict[str, Any]) -> dict[str, Any]:
        """Transfer length from non-leaf to children (leaf-only constraint)."""
        if not tree_data.get("children"):
            return tree_data

        parent_length = tree_data.get("length")
        children = tree_data["children"]

        if parent_length is not None and children:
            for child in children:
                child["length"] = parent_length
            tree_data["length"] = None

        tree_data["children"] = [
            TreeService.transfer_length_to_leaves(child) for child in children
        ]

        return tree_data
