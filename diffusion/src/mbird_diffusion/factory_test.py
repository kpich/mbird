"""Tests for factory functions."""

import pytest

from mbird_diffusion.expander import AudioDiffusionExpander
from mbird_diffusion.factory import get_expander, get_inpainter
from mbird_diffusion.inpainter import AudioDiffusionInpainter


def test_get_inpainter_returns_default_implementation() -> None:
    """get_inpainter with default returns AudioDiffusionInpainter."""
    inpainter = get_inpainter()

    assert isinstance(inpainter, AudioDiffusionInpainter)


def test_get_inpainter_accepts_explicit_model_name() -> None:
    """get_inpainter accepts explicit model name."""
    inpainter = get_inpainter(model_name="audio-diffusion")

    assert isinstance(inpainter, AudioDiffusionInpainter)


def test_get_inpainter_raises_on_unknown_model() -> None:
    """get_inpainter raises ValueError for unknown model names."""
    with pytest.raises(ValueError, match="Unknown inpainter model"):
        get_inpainter(model_name="nonexistent")  # type: ignore


def test_get_expander_returns_default_implementation() -> None:
    """get_expander with default returns AudioDiffusionExpander."""
    expander = get_expander()

    assert isinstance(expander, AudioDiffusionExpander)


def test_get_expander_accepts_explicit_model_name() -> None:
    """get_expander accepts explicit model name."""
    expander = get_expander(model_name="audio-diffusion")

    assert isinstance(expander, AudioDiffusionExpander)


def test_get_expander_raises_on_unknown_model() -> None:
    """get_expander raises ValueError for unknown model names."""
    with pytest.raises(ValueError, match="Unknown expander model"):
        get_expander(model_name="nonexistent")  # type: ignore


def test_factory_functions_accept_device_parameter() -> None:
    """Factory functions pass through device parameter to implementations."""
    inpainter = get_inpainter(device="cpu")
    expander = get_expander(device="cpu")

    assert inpainter.device.type == "cpu"
    assert expander.device.type == "cpu"
