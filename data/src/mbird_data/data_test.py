import json
from pathlib import Path

import pytest

from mbird_data import MbirdData, MbirdNode
from mbird_data.constants import TREE_FNAME


def test_node_data_preserved_across_serialization():
    grandchild = MbirdNode(id="grandchild1")
    child = MbirdNode(id="child1", children=[grandchild])
    root = MbirdNode(id="root", children=[child])

    json_str = json.dumps(root.model_dump())
    restored_root = MbirdNode(**json.loads(json_str))

    assert restored_root.id == "root"
    assert len(restored_root.children) == 1
    assert restored_root.children[0].id == "child1"
    assert restored_root.children[0].children[0].id == "grandchild1"


def test_data_preserved_across_save_and_load(tmp_path: Path):
    data = MbirdData()
    node2 = MbirdNode(id="node2")
    node1 = MbirdNode(id="node1", children=[node2])
    data.root = MbirdNode(id="root", children=[node1])

    mbird_dir = tmp_path / "test_dir"
    data.save(mbird_dir)

    assert (mbird_dir / TREE_FNAME).exists()

    loaded_data = MbirdData()
    loaded_data.load(mbird_dir)

    assert loaded_data.root.id == "root"
    assert len(loaded_data.root.children) == 1
    assert loaded_data.root.children[0].id == "node1"
    assert loaded_data.root.children[0].children[0].id == "node2"


def test_loading_nonexistent_directory_raises_error():
    data = MbirdData()
    with pytest.raises(FileNotFoundError):
        data.load("/nonexistent/path")


def test_saving_without_root_raises_error(tmp_path: Path):
    data = MbirdData()
    with pytest.raises(ValueError, match="No root node loaded"):
        data.save(tmp_path / "test_dir")


def test_loading_cyclic_tree_raises_error():
    cyclic_dict = {
        "id": "node1",
        "children": [
            {
                "id": "node2",
                "children": [{"id": "node1", "children": []}],
            }
        ],
    }

    with pytest.raises(ValueError, match="Cycle detected"):
        MbirdNode(**cyclic_dict)


def test_saving_creates_nested_directories(tmp_path: Path):
    data = MbirdData()
    data.root = MbirdNode(id="root")

    nested_dir = tmp_path / "deeply" / "nested" / "path"
    data.save(nested_dir)

    assert nested_dir.exists()
    assert (nested_dir / TREE_FNAME).exists()
