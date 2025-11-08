from typing import Any

from mbird_audiogen import MbirdGenerator
from mbird_data import MbirdData, MbirdNode


class TreeService:
    """Manages tree operations and transformations."""

    # Audio generator instance
    _generator = MbirdGenerator()

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
        """Run generate() to set is_stale=False for all nodes and concatenate clips."""
        if data.root is None:
            raise ValueError("No root node in project data")

        # Generate individual clips for stale nodes
        TreeService.generate(data.root, data)

        # Get leaf nodes in order and concatenate their clips
        leaf_nodes = TreeService.get_leaf_nodes_in_order(data.root)
        clip_paths = []

        for leaf_node in leaf_nodes:
            if leaf_node.sound_file:  # Only include nodes with generated audio
                clip_path = data.get_clip_path(leaf_node.id)
                clip_paths.append(clip_path)

        # Create concatenated output file
        if clip_paths and data.directory:
            output_path = data.directory / "cur.wav"
            TreeService._generator.concatenate_leaf_nodes(clip_paths, output_path)

        return data

    @staticmethod
    def generate(node: MbirdNode, data: MbirdData) -> None:
        """Recursively set is_stale=False and generate audio for stale leaf nodes."""
        if node.is_stale and not node.children:
            # Leaf node that is stale - generate audio
            TreeService._generate_audio(node, data)

        node.is_stale = False
        for child in node.children:
            TreeService.generate(child, data)

    @staticmethod
    def _generate_audio(node: MbirdNode, data: MbirdData) -> None:
        """Generate audio file for a node using MbirdGenerator."""
        # Get clip path from data
        clip_path = data.get_clip_path(node.id)

        # Generate audio using the generator
        TreeService._generator.generate_node_audio(node, clip_path)

        # Set sound_file reference
        node.sound_file = f"{node.id}.wav"

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

    @staticmethod
    def get_leaf_nodes_in_order(node: MbirdNode) -> list[MbirdNode]:
        """Get leaf nodes in depth-first traversal order.

        Args:
            node: Root node to start traversal from

        Returns:
            List of leaf nodes in traversal order
        """
        leaf_nodes = []

        def traverse(current_node: MbirdNode):
            if not current_node.children:
                # This is a leaf node
                leaf_nodes.append(current_node)
            else:
                # Traverse children in order
                for child in current_node.children:
                    traverse(child)

        traverse(node)
        return leaf_nodes
