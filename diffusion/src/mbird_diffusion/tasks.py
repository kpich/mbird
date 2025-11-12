"""Abstract task interfaces for audio diffusion models.

These protocols define the task signatures without coupling to specific model
implementations. This allows easy swapping of underlying models.
"""

from typing import Protocol

import numpy as np


class AudioInpainter(Protocol):
    """Protocol for audio inpainting/infilling models.

    Inpainting fills gaps between audio segments, smoothing transitions.
    """

    def inpaint(
        self,
        audio1: np.ndarray,
        audio2: np.ndarray,
        gap_duration: float,
        sample_rate: int = 44100,
    ) -> np.ndarray:
        """Fill the gap between two audio segments with smooth transitions.

        Args:
            audio1: First audio segment (shape: [samples] or [channels, samples])
            audio2: Second audio segment (shape: [samples] or [channels, samples])
            gap_duration: Duration in seconds to generate between segments
            sample_rate: Sample rate in Hz (default: 44100)

        Returns:
            Complete audio with audio1, generated gap, and audio2 concatenated
            (shape matches input shape)
        """
        ...


class AudioExpander(Protocol):
    """Protocol for audio expansion/extrapolation models.

    Expansion extends short audio clips to longer durations.
    """

    def expand(
        self,
        audio: np.ndarray,
        target_duration: float,
        sample_rate: int = 44100,
    ) -> np.ndarray:
        """Expand a short audio clip to a longer target duration.

        Args:
            audio: Input audio segment (shape: [samples] or [channels, samples])
            target_duration: Desired output duration in seconds
            sample_rate: Sample rate in Hz (default: 44100)

        Returns:
            Expanded audio of target_duration length (shape matches input shape)
        """
        ...
