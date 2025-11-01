import json
from pathlib import Path

from pydantic import BaseModel, Field, model_validator

from mbird_data.models import MbirdNode


class MbirdTree(BaseModel):
    root_id: str | None = None
    nodes: dict[str, MbirdNode] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_acyclic(self):
        """Ensure the tree structure is acyclic (is a DAG)."""
        visited = set()
        visiting = set()

        def has_cycle(node_id: str) -> bool:
            if node_id in visiting:
                return True
            if node_id in visited:
                return False
            if node_id not in self.nodes:
                return False

            visiting.add(node_id)
            node = self.nodes[node_id]
            for child_id in node.children:
                if has_cycle(child_id):
                    return True
            visiting.remove(node_id)
            visited.add(node_id)
            return False

        for node_id in self.nodes:
            if has_cycle(node_id):
                raise ValueError(f"Cycle detected in tree involving node: {node_id}")

        return self

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
        nodes_dict = {
            node_data["id"]: MbirdNode(**node_data)
            for node_data in data.get("nodes", [])
        }
        return cls(root_id=data.get("root_id"), nodes=nodes_dict)

    @classmethod
    def from_json(cls, json_str: str) -> "MbirdTree":
        """Deserialize tree from JSON string."""
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def load(cls, file_path: Path) -> "MbirdTree":
        """Load tree from JSON file."""
        return cls.from_json(file_path.read_text())
