"""Audio diffusion models for mbird.

This package provides audio interpolation and extrapolation capabilities using
diffusion models. Models can be easily swapped via the factory functions.

Example usage:
    from mbird_diffusion import get_interpolator, get_extrapolator

    # Get models
    interpolator = get_interpolator()
    extrapolator = get_extrapolator()

    # Interpolate between two audio segments
    result = interpolator.interpolate(audio1, audio2, gap_duration=2.0)

    # Extrapolate short clip to longer duration
    extrapolated = extrapolator.extrapolate(audio, target_duration=10.0)
"""

from mbird_diffusion.extrapolator import AudioDiffusionExtrapolator
from mbird_diffusion.factory import get_extrapolator, get_interpolator
from mbird_diffusion.interpolator import AudioDiffusionInterpolator
from mbird_diffusion.tasks import AudioExtrapolator, AudioInterpolator

__all__ = [
    # Factory functions (main API)
    "get_interpolator",
    "get_extrapolator",
    # Protocols (for type hints)
    "AudioInterpolator",
    "AudioExtrapolator",
    # Concrete implementations (for direct use if needed)
    "AudioDiffusionInterpolator",
    "AudioDiffusionExtrapolator",
]
