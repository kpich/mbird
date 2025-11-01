from pydantic import BaseModel, Field, model_validator


class MbirdNode(BaseModel):
    id: str
    children: list["MbirdNode"] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_acyclic(self):
        """Ensure the tree structure is acyclic (is a DAG)."""
        visited = set()

        def has_cycle(node: "MbirdNode", visiting: set[str]) -> bool:
            if node.id in visiting:
                return True
            if node.id in visited:
                return False

            new_visiting = visiting | {node.id}
            for child in node.children:
                if has_cycle(child, new_visiting):
                    return True
            visited.add(node.id)
            return False

        if has_cycle(self, set()):
            raise ValueError(f"Cycle detected in tree involving node: {self.id}")

        return self
