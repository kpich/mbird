from pathlib import Path

import pytest

from mbird_data import MbirdData, MbirdNode, MbirdTree


def test_tree_data_preserved_across_serialization(tmp_path: Path):
    tree = MbirdTree(root_id="root")
    tree.add_node(MbirdNode(id="root", properties={"name": "Root Node"}))
    tree.add_node(
        MbirdNode(
            id="child1",
            properties={"name": "Child 1"},
            children=["grandchild1"],
        )
    )
    tree.add_node(
        MbirdNode(
            id="grandchild1",
            properties={"name": "Grandchild 1"},
            references=["root"],
        )
    )

    json_str = tree.to_json()
    restored_tree = MbirdTree.from_json(json_str)

    assert restored_tree.root_id == "root"
    assert len(restored_tree.nodes) == 3
    assert restored_tree.get_node("root").properties["name"] == "Root Node"
    assert restored_tree.get_node("child1").children == ["grandchild1"]
    assert restored_tree.get_node("grandchild1").references == ["root"]


def test_data_preserved_across_save_and_load(tmp_path: Path):
    data = MbirdData()
    data.tree = MbirdTree(root_id="root")
    data.tree.add_node(MbirdNode(id="root", properties={"type": "root"}))
    data.tree.add_node(
        MbirdNode(
            id="node1",
            properties={"type": "leaf", "value": 42},
            references=["root"],
        )
    )

    mbird_dir = tmp_path / "test.mbird"
    data.save(mbird_dir)

    assert (mbird_dir / "tree.json").exists()

    loaded_data = MbirdData()
    loaded_data.load(mbird_dir)

    assert loaded_data.tree.root_id == "root"
    assert len(loaded_data.tree.nodes) == 2
    assert loaded_data.tree.get_node("node1").properties["value"] == 42


def test_resolve_references_returns_actual_nodes():
    tree = MbirdTree()
    node1 = MbirdNode(id="node1")
    node2 = MbirdNode(id="node2", references=["node1"])
    tree.add_node(node1)
    tree.add_node(node2)

    refs = tree.resolve_references("node2")

    assert len(refs) == 1
    assert refs[0].id == "node1"


def test_loading_nonexistent_directory_raises_error():
    data = MbirdData()
    with pytest.raises(FileNotFoundError):
        data.load("/nonexistent/path.mbird")


def test_saving_without_tree_raises_error(tmp_path: Path):
    data = MbirdData()
    with pytest.raises(ValueError, match="No tree loaded"):
        data.save(tmp_path / "test.mbird")
