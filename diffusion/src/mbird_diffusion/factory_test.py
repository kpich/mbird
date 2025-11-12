"""Tests for factory functions."""

import pytest

from mbird_diffusion.extrapolator import AudioDiffusionExtrapolator
from mbird_diffusion.factory import get_extrapolator, get_interpolator
from mbird_diffusion.interpolator import AudioDiffusionInterpolator


def test_get_interpolator_returns_default_implementation() -> None:
    """get_interpolator with default returns AudioDiffusionInterpolator."""
    interpolator = get_interpolator()

    assert isinstance(interpolator, AudioDiffusionInterpolator)


def test_get_interpolator_accepts_explicit_model_name() -> None:
    """get_interpolator accepts explicit model name."""
    interpolator = get_interpolator(model_name="audio-diffusion")

    assert isinstance(interpolator, AudioDiffusionInterpolator)


def test_get_interpolator_raises_on_unknown_model() -> None:
    """get_interpolator raises ValueError for unknown model names."""
    with pytest.raises(ValueError, match="Unknown interpolator model"):
        get_interpolator(model_name="nonexistent")  # type: ignore


def test_get_extrapolator_returns_default_implementation() -> None:
    """get_extrapolator with default returns AudioDiffusionExtrapolator."""
    extrapolator = get_extrapolator()

    assert isinstance(extrapolator, AudioDiffusionExtrapolator)


def test_get_extrapolator_accepts_explicit_model_name() -> None:
    """get_extrapolator accepts explicit model name."""
    extrapolator = get_extrapolator(model_name="audio-diffusion")

    assert isinstance(extrapolator, AudioDiffusionExtrapolator)


def test_get_extrapolator_raises_on_unknown_model() -> None:
    """get_extrapolator raises ValueError for unknown model names."""
    with pytest.raises(ValueError, match="Unknown extrapolator model"):
        get_extrapolator(model_name="nonexistent")  # type: ignore


def test_factory_functions_accept_device_parameter() -> None:
    """Factory functions pass through device parameter to implementations."""
    interpolator = get_interpolator(device="cpu")
    extrapolator = get_extrapolator(device="cpu")

    assert interpolator.device.type == "cpu"
    assert extrapolator.device.type == "cpu"
