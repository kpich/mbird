"""Factory functions for creating audio diffusion models.

This module provides a simple registry system for swapping model implementations
without changing calling code.
"""

from typing import Literal

from mbird_diffusion.expander import AudioDiffusionExpander
from mbird_diffusion.inpainter import AudioDiffusionInpainter
from mbird_diffusion.tasks import AudioExpander, AudioInpainter

# Type aliases for available model names
InpainterModel = Literal["audio-diffusion", "default"]
ExpanderModel = Literal["audio-diffusion", "default"]


def get_inpainter(
    model_name: InpainterModel = "default", device: str | None = None
) -> AudioInpainter:
    """Get an audio inpainter model by name.

    Args:
        model_name: Name of the model to use. Options:
            - "audio-diffusion" or "default": AudioDiffusionInpainter
        device: Device to run inference on (None for auto-detect)

    Returns:
        An AudioInpainter instance

    Raises:
        ValueError: If model_name is not recognized
    """
    if model_name in ("audio-diffusion", "default"):
        return AudioDiffusionInpainter(device=device)
    else:
        raise ValueError(
            f"Unknown inpainter model: {model_name}. "
            f"Available: 'audio-diffusion', 'default'"
        )


def get_expander(
    model_name: ExpanderModel = "default", device: str | None = None
) -> AudioExpander:
    """Get an audio expander model by name.

    Args:
        model_name: Name of the model to use. Options:
            - "audio-diffusion" or "default": AudioDiffusionExpander
        device: Device to run inference on (None for auto-detect)

    Returns:
        An AudioExpander instance

    Raises:
        ValueError: If model_name is not recognized
    """
    if model_name in ("audio-diffusion", "default"):
        return AudioDiffusionExpander(device=device)
    else:
        raise ValueError(
            f"Unknown expander model: {model_name}. "
            f"Available: 'audio-diffusion', 'default'"
        )
