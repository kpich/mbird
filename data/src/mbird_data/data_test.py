from pathlib import Path

import pytest

from mbird_data import MbirdData, MbirdNode
from mbird_data.constants import TREE_FNAME


def test_data_preserved_across_save_and_load(tmp_path: Path):
    node2 = MbirdNode(id="node2")
    node1 = MbirdNode(id="node1", children=[node2])
    root = MbirdNode(id="root", children=[node1])
    data = MbirdData(root=root)

    mbird_dir = tmp_path / "test_dir.mbird"
    data.save(mbird_dir)

    assert (mbird_dir / TREE_FNAME).exists()

    loaded_data = MbirdData.load(mbird_dir)

    assert loaded_data.root is not None
    assert loaded_data.root.id == "root"
    assert len(loaded_data.root.children) == 1
    assert loaded_data.root.children[0].id == "node1"
    assert loaded_data.root.children[0].children[0].id == "node2"


def test_loading_nonexistent_directory_raises_error():
    with pytest.raises(FileNotFoundError):
        MbirdData.load("/nonexistent/path.mbird")


def test_loading_without_mbird_extension_raises_error():
    with pytest.raises(ValueError, match="must have .mbird extension"):
        MbirdData.load("/some/path")


def test_saving_without_root_raises_error(tmp_path: Path):
    data = MbirdData()
    with pytest.raises(ValueError, match="No root node loaded"):
        data.save(tmp_path / "test_dir.mbird")


def test_save_appends_mbird_extension_if_missing(tmp_path: Path):
    root = MbirdNode(id="root")
    data = MbirdData(root=root)

    dir_without_ext = tmp_path / "myproject"
    data.save(dir_without_ext)

    expected_dir = tmp_path / "myproject.mbird"
    assert expected_dir.exists()
    assert (expected_dir / TREE_FNAME).exists()


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
        MbirdNode(**cyclic_dict)  # type: ignore[arg-type]


def test_saving_creates_nested_directories(tmp_path: Path):
    root = MbirdNode(id="root")
    data = MbirdData(root=root)

    nested_dir = tmp_path / "deeply" / "nested" / "path.mbird"
    data.save(nested_dir)

    assert nested_dir.exists()
    assert (nested_dir / TREE_FNAME).exists()


def test_is_stale_defaults_to_true():
    node = MbirdNode(id="test")
    assert node.is_stale is True


def test_is_stale_preserved_across_save_and_load(tmp_path: Path):
    node = MbirdNode(id="node1", is_stale=False)
    root = MbirdNode(id="root", children=[node])
    data = MbirdData(root=root)

    mbird_dir = tmp_path / "test_stale.mbird"
    data.save(mbird_dir)

    loaded_data = MbirdData.load(mbird_dir)

    assert loaded_data.root is not None
    assert loaded_data.root.is_stale is True
    assert loaded_data.root.children[0].is_stale is False
