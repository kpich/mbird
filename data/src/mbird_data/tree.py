import json
from pathlib import Path

from mbird_data.models import MbirdNode


class MbirdTree:
    def __init__(self, root_id: str | None = None):
        self.nodes: dict[str, MbirdNode] = {}
        self.root_id = root_id

    def add_node(self, node: MbirdNode) -> None:
        """Add a node to the tree."""
        self.nodes[node.id] = node

    def to_dict(self) -> dict:
        """Serialize tree to dictionary."""
        return {
            "root_id": self.root_id,
            "nodes": [node.model_dump() for node in self.nodes.values()],
        }

    def to_json(self) -> str:
        """Serialize tree to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    def save(self, file_path: Path) -> None:
        """Save tree to JSON file."""
        file_path.write_text(self.to_json())

    @classmethod
    def from_dict(cls, data: dict) -> "MbirdTree":
        """Deserialize tree from dictionary."""
        tree = cls(root_id=data.get("root_id"))
        for node_data in data.get("nodes", []):
            tree.add_node(MbirdNode(**node_data))
        return tree

    @classmethod
    def from_json(cls, json_str: str) -> "MbirdTree":
        """Deserialize tree from JSON string."""
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def load(cls, file_path: Path) -> "MbirdTree":
        """Load tree from JSON file."""
        return cls.from_json(file_path.read_text())
