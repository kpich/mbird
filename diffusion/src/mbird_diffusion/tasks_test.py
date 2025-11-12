"""Tests for task protocol interfaces."""

import numpy as np

from mbird_diffusion.tasks import AudioExtrapolator, AudioInterpolator


def test_interpolator_protocol_is_callable_with_correct_signature() -> None:
    """AudioInterpolator protocol accepts standard interpolate call signature."""

    class MockInterpolator:
        def interpolate(
            self,
            audio1: np.ndarray,
            audio2: np.ndarray,
            gap_duration: float,
            sample_rate: int = 44100,
        ) -> np.ndarray:
            return np.concatenate([audio1, audio2])

    interpolator: AudioInterpolator = MockInterpolator()
    audio1 = np.zeros(1000)
    audio2 = np.zeros(1000)

    result = interpolator.interpolate(audio1, audio2, gap_duration=1.0)

    assert result.shape == (2000,)


def test_extrapolator_protocol_is_callable_with_correct_signature() -> None:
    """AudioExtrapolator protocol accepts standard extrapolate call signature."""

    class MockExtrapolator:
        def extrapolate(
            self,
            audio: np.ndarray,
            target_duration: float,
            sample_rate: int = 44100,
        ) -> np.ndarray:
            target_samples = int(target_duration * sample_rate)
            return np.zeros(target_samples)

    extrapolator: AudioExtrapolator = MockExtrapolator()
    audio = np.zeros(1000)

    result = extrapolator.extrapolate(audio, target_duration=2.0)

    assert result.shape == (2 * 44100,)
