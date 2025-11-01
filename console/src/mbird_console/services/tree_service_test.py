from typing import Any

from mbird_data import MbirdData, MbirdNode
import pytest

from mbird_console.services.tree_service import TreeService


def test_get_tree_returns_tree_data():
    root = MbirdNode(id="root", length=None, children=[])
    data = MbirdData(root=root)

    tree_dict = TreeService.get_tree(data)

    assert tree_dict["id"] == "root"
    assert tree_dict["children"] == []


def test_update_tree_with_valid_data_succeeds():
    new_tree = {
        "id": "root",
        "length": None,
        "children": [
            {"id": "child1", "length": 10.0, "children": []},
            {"id": "child2", "length": 5.0, "children": []},
        ],
    }

    data = TreeService.update_tree(new_tree)

    assert data.root is not None
    assert len(data.root.children) == 2
    assert data.root.children[0].id == "child1"
    assert data.root.children[1].id == "child2"


def test_update_tree_with_cyclic_data_raises_error():
    cyclic_tree = {
        "id": "node1",
        "length": None,
        "children": [
            {
                "id": "node2",
                "length": None,
                "children": [{"id": "node1", "length": 10.0, "children": []}],
            }
        ],
    }

    with pytest.raises(ValueError, match="Cycle detected"):
        TreeService.update_tree(cyclic_tree)


def test_update_tree_with_invalid_structure_raises_error():
    invalid_tree: dict[str, Any] = {"children": [], "length": None}

    with pytest.raises(ValueError):
        TreeService.update_tree(invalid_tree)


def test_regenerate_sets_is_stale_false_for_all_nodes():
    child1 = MbirdNode(id="child1", length=10.0, is_stale=True)
    child2 = MbirdNode(id="child2", length=5.0, is_stale=True)
    root = MbirdNode(id="root", length=None, children=[child1, child2], is_stale=True)
    data = MbirdData(root=root)

    TreeService.regenerate(data)

    assert data.root is not None
    assert data.root.is_stale is False
    assert data.root.children[0].is_stale is False
    assert data.root.children[1].is_stale is False


def test_transfer_length_to_leaves_transfers_parent_length_to_child():
    tree_with_new_child = {
        "id": "root",
        "length": 15.0,
        "children": [{"id": "new_child", "length": 10.0, "children": []}],
    }

    result = TreeService.transfer_length_to_leaves(tree_with_new_child)

    assert result["length"] is None
    assert result["children"][0]["length"] == 15.0


def test_generate_recursively_sets_is_stale_false():
    child1 = MbirdNode(id="child1", length=10.0, is_stale=True)
    child2 = MbirdNode(id="child2", length=5.0, is_stale=True)
    root = MbirdNode(id="root", length=None, children=[child1, child2], is_stale=True)

    TreeService.generate(root)

    assert root.is_stale is False
    assert child1.is_stale is False
    assert child2.is_stale is False
