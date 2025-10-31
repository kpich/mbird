from typing import Any


def load_graph(file_path: str) -> dict[str, Any]:
    """
    Load graph from file.
    Format TBD - placeholder returns sample graph.
    """
    return {
        "nodes": [
            {"id": "1", "position": {"x": 100, "y": 100}, "data": {"label": "Node 1"}},
            {"id": "2", "position": {"x": 300, "y": 100}, "data": {"label": "Node 2"}},
        ],
        "edges": [
            {"id": "e1-2", "source": "1", "target": "2"},
        ],
    }


def save_graph(file_path: str, graph_data: dict[str, Any]) -> None:
    """
    Save graph to file.
    Format TBD - placeholder does nothing.
    """
    pass
