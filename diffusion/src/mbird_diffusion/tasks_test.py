"""Tests for task protocol interfaces."""

import numpy as np

from mbird_diffusion.tasks import AudioExpander, AudioInpainter


def test_inpainter_protocol_is_callable_with_correct_signature() -> None:
    """AudioInpainter protocol accepts standard inpaint call signature."""

    class MockInpainter:
        def inpaint(
            self,
            audio1: np.ndarray,
            audio2: np.ndarray,
            gap_duration: float,
            sample_rate: int = 44100,
        ) -> np.ndarray:
            return np.concatenate([audio1, audio2])

    inpainter: AudioInpainter = MockInpainter()
    audio1 = np.zeros(1000)
    audio2 = np.zeros(1000)

    result = inpainter.inpaint(audio1, audio2, gap_duration=1.0)

    assert result.shape == (2000,)


def test_expander_protocol_is_callable_with_correct_signature() -> None:
    """AudioExpander protocol accepts standard expand call signature."""

    class MockExpander:
        def expand(
            self,
            audio: np.ndarray,
            target_duration: float,
            sample_rate: int = 44100,
        ) -> np.ndarray:
            target_samples = int(target_duration * sample_rate)
            return np.zeros(target_samples)

    expander: AudioExpander = MockExpander()
    audio = np.zeros(1000)

    result = expander.expand(audio, target_duration=2.0)

    assert result.shape == (2 * 44100,)
