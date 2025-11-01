from pathlib import Path

import pytest

from mbird_data import MbirdData, MbirdNode, MbirdTree


def test_tree_data_preserved_across_serialization(tmp_path: Path):
    tree = MbirdTree(root_id="root")
    tree.add_node(MbirdNode(id="root"))
    tree.add_node(MbirdNode(id="child1", children=["grandchild1"]))
    tree.add_node(MbirdNode(id="grandchild1"))

    json_str = tree.to_json()
    restored_tree = MbirdTree.from_json(json_str)

    assert restored_tree.root_id == "root"
    assert len(restored_tree.nodes) == 3
    assert "root" in restored_tree.nodes
    assert restored_tree.nodes["child1"].children == ["grandchild1"]
    assert restored_tree.nodes["grandchild1"].children == []


def test_data_preserved_across_save_and_load(tmp_path: Path):
    data = MbirdData()
    data.tree = MbirdTree(root_id="root")
    data.tree.add_node(MbirdNode(id="root"))
    data.tree.add_node(MbirdNode(id="node1", children=["node2"]))
    data.tree.add_node(MbirdNode(id="node2"))

    mbird_dir = tmp_path / "test.mbird"
    data.save(mbird_dir)

    assert (mbird_dir / "tree.json").exists()

    loaded_data = MbirdData()
    loaded_data.load(mbird_dir)

    assert loaded_data.tree.root_id == "root"
    assert len(loaded_data.tree.nodes) == 3
    assert loaded_data.tree.nodes["node1"].children == ["node2"]


def test_loading_nonexistent_directory_raises_error():
    data = MbirdData()
    with pytest.raises(FileNotFoundError):
        data.load("/nonexistent/path.mbird")


def test_saving_without_tree_raises_error(tmp_path: Path):
    data = MbirdData()
    with pytest.raises(ValueError, match="No tree loaded"):
        data.save(tmp_path / "test.mbird")


def test_loading_cyclic_tree_raises_error():
    cyclic_data = {
        "root_id": "node1",
        "nodes": [
            {"id": "node1", "children": ["node2"]},
            {"id": "node2", "children": ["node1"]},
        ],
    }

    with pytest.raises(ValueError, match="Cycle detected"):
        MbirdTree.from_dict(cyclic_data)
