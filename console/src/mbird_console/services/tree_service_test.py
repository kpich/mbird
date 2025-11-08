from typing import Any
from unittest.mock import Mock, patch

import pytest

from mbird_console.services.tree_service import TreeService
from mbird_data import MbirdData, MbirdNode


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


def test_regenerate_sets_is_stale_false_for_all_nodes(tmp_path):
    child1 = MbirdNode(id="child1", length=10.0, is_stale=True)
    child2 = MbirdNode(id="child2", length=5.0, is_stale=True)
    root = MbirdNode(id="root", length=None, children=[child1, child2], is_stale=True)
    project_dir = tmp_path / "test.mbird"
    data = MbirdData(root=root, directory=project_dir)

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


def test_generate_recursively_sets_is_stale_false(tmp_path):
    child1 = MbirdNode(id="child1", length=10.0, is_stale=True)
    child2 = MbirdNode(id="child2", length=5.0, is_stale=True)
    root = MbirdNode(id="root", length=None, children=[child1, child2], is_stale=True)
    project_dir = tmp_path / "test.mbird"
    data = MbirdData(root=root, directory=project_dir)

    TreeService.generate(root, data)

    assert root.is_stale is False
    assert child1.is_stale is False
    assert child2.is_stale is False


def test_generate_calls_audio_generator_for_stale_leaf_nodes(tmp_path):
    """Unit test: verify TreeService calls MbirdGenerator without actual I/O."""
    child1 = MbirdNode(id="child1", length=2.0, is_stale=True)
    child2 = MbirdNode(id="child2", length=1.5, is_stale=True)
    root = MbirdNode(id="root", length=None, children=[child1, child2], is_stale=True)
    project_dir = tmp_path / "test.mbird"
    data = MbirdData(root=root, directory=project_dir)

    # Mock the generator
    mock_generator = Mock()
    with patch.object(TreeService, "_generator", mock_generator):
        TreeService.regenerate(data)

    # Verify audio generator was called for leaf nodes
    assert mock_generator.generate_node_audio.call_count == 2

    # Verify correct arguments
    calls = mock_generator.generate_node_audio.call_args_list
    assert calls[0][0][0].id == "child1"  # First arg is node
    assert calls[0][0][1] == project_dir / "clips" / "child1.wav"  # Second is path

    assert calls[1][0][0].id == "child2"
    assert calls[1][0][1] == project_dir / "clips" / "child2.wav"

    # Verify sound_file was set
    assert data.root is not None
    assert data.root.children[0].sound_file == "child1.wav"
    assert data.root.children[1].sound_file == "child2.wav"


def test_get_leaf_nodes_returns_single_node_when_root_is_leaf():
    root = MbirdNode(id="root", length=10.0)

    leaf_nodes = TreeService.get_leaf_nodes_in_order(root)

    assert len(leaf_nodes) == 1
    assert leaf_nodes[0].id == "root"


def test_get_leaf_nodes_returns_children_in_left_to_right_order():
    child1 = MbirdNode(id="left", length=5.0)
    child2 = MbirdNode(id="right", length=3.0)
    root = MbirdNode(id="root", length=None, children=[child1, child2])

    leaf_nodes = TreeService.get_leaf_nodes_in_order(root)

    assert len(leaf_nodes) == 2
    assert leaf_nodes[0].id == "left"
    assert leaf_nodes[1].id == "right"


def test_get_leaf_nodes_prioritizes_deeper_left_over_shallow_right():
    # Left subtree: root -> left -> deep_left
    deep_left = MbirdNode(id="deep_left", length=2.0)
    left = MbirdNode(id="left", length=None, children=[deep_left])

    # Right subtree: root -> right (leaf)
    right = MbirdNode(id="right", length=4.0)

    root = MbirdNode(id="root", length=None, children=[left, right])

    leaf_nodes = TreeService.get_leaf_nodes_in_order(root)

    assert len(leaf_nodes) == 2
    assert leaf_nodes[0].id == "deep_left"  # Deep left comes first
    assert leaf_nodes[1].id == "right"  # Shallow right comes second


def test_get_leaf_nodes_handles_mixed_depth_tree_correctly():
    # Complex tree:
    #       root
    #      /    \
    #   left     right
    #   /  \       \
    # l1   l2      r1
    #             /  \
    #           r1a  r1b

    l1 = MbirdNode(id="l1", length=1.0)
    l2 = MbirdNode(id="l2", length=2.0)
    left = MbirdNode(id="left", length=None, children=[l1, l2])

    r1a = MbirdNode(id="r1a", length=3.0)
    r1b = MbirdNode(id="r1b", length=4.0)
    r1 = MbirdNode(id="r1", length=None, children=[r1a, r1b])
    right = MbirdNode(id="right", length=None, children=[r1])

    root = MbirdNode(id="root", length=None, children=[left, right])

    leaf_nodes = TreeService.get_leaf_nodes_in_order(root)

    assert len(leaf_nodes) == 4
    assert leaf_nodes[0].id == "l1"  # Left subtree first
    assert leaf_nodes[1].id == "l2"  # Left subtree second
    assert leaf_nodes[2].id == "r1a"  # Right subtree third
    assert leaf_nodes[3].id == "r1b"  # Right subtree fourth


def test_get_leaf_nodes_skips_non_leaf_nodes():
    leaf1 = MbirdNode(id="leaf1", length=1.0)
    leaf2 = MbirdNode(id="leaf2", length=2.0)
    internal = MbirdNode(id="internal", length=None, children=[leaf2])
    root = MbirdNode(id="root", length=None, children=[leaf1, internal])

    leaf_nodes = TreeService.get_leaf_nodes_in_order(root)

    assert len(leaf_nodes) == 2
    assert leaf_nodes[0].id == "leaf1"  # Direct leaf
    assert leaf_nodes[1].id == "leaf2"  # Leaf through internal node
    # "root" and "internal" should not be in results
