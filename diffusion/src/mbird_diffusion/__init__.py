"""Audio diffusion models for mbird.

This package provides audio inpainting and expansion capabilities using
diffusion models. Models can be easily swapped via the factory functions.

Example usage:
    from mbird_diffusion import get_inpainter, get_expander

    # Get models
    inpainter = get_inpainter()
    expander = get_expander()

    # Inpaint between two audio segments
    result = inpainter.inpaint(audio1, audio2, gap_duration=2.0)

    # Expand short clip to longer duration
    expanded = expander.expand(audio, target_duration=10.0)
"""

from mbird_diffusion.expander import AudioDiffusionExpander
from mbird_diffusion.factory import get_expander, get_inpainter
from mbird_diffusion.inpainter import AudioDiffusionInpainter
from mbird_diffusion.tasks import AudioExpander, AudioInpainter

__all__ = [
    # Factory functions (main API)
    "get_inpainter",
    "get_expander",
    # Protocols (for type hints)
    "AudioInpainter",
    "AudioExpander",
    # Concrete implementations (for direct use if needed)
    "AudioDiffusionInpainter",
    "AudioDiffusionExpander",
]
