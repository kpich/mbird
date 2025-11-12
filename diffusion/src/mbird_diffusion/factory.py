"""Factory functions for creating audio diffusion models.

This module provides a simple registry system for swapping model implementations
without changing calling code.
"""

from typing import Literal

from mbird_diffusion.extrapolator import AudioDiffusionExtrapolator
from mbird_diffusion.interpolator import AudioDiffusionInterpolator
from mbird_diffusion.tasks import AudioExtrapolator, AudioInterpolator

# Type aliases for available model names
InterpolatorModel = Literal["audio-diffusion", "default"]
ExtrapolatorModel = Literal["audio-diffusion", "default"]


def get_interpolator(
    model_name: InterpolatorModel = "default", device: str | None = None
) -> AudioInterpolator:
    """Get an audio interpolator model by name.

    Args:
        model_name: Name of the model to use. Options:
            - "audio-diffusion" or "default": AudioDiffusionInterpolator
        device: Device to run inference on (None for auto-detect)

    Returns:
        An AudioInterpolator instance

    Raises:
        ValueError: If model_name is not recognized
    """
    if model_name in ("audio-diffusion", "default"):
        return AudioDiffusionInterpolator(device=device)
    else:
        raise ValueError(
            f"Unknown interpolator model: {model_name}. "
            f"Available: 'audio-diffusion', 'default'"
        )


def get_extrapolator(
    model_name: ExtrapolatorModel = "default", device: str | None = None
) -> AudioExtrapolator:
    """Get an audio extrapolator model by name.

    Args:
        model_name: Name of the model to use. Options:
            - "audio-diffusion" or "default": AudioDiffusionExtrapolator
        device: Device to run inference on (None for auto-detect)

    Returns:
        An AudioExtrapolator instance

    Raises:
        ValueError: If model_name is not recognized
    """
    if model_name in ("audio-diffusion", "default"):
        return AudioDiffusionExtrapolator(device=device)
    else:
        raise ValueError(
            f"Unknown extrapolator model: {model_name}. "
            f"Available: 'audio-diffusion', 'default'"
        )
