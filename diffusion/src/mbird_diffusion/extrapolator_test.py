"""Tests for audio extrapolation implementations."""

import numpy as np

from mbird_diffusion.extrapolator import AudioDiffusionExtrapolator


def test_extrapolator_returns_audio_with_target_duration() -> None:
    """Extrapolator produces audio of the requested target duration."""
    extrapolator = AudioDiffusionExtrapolator(device="cpu")

    sample_rate = 1000
    audio = np.sin(2 * np.pi * 440 * np.linspace(0, 1, sample_rate))
    target_duration = 3.0

    result = extrapolator.extrapolate(audio, target_duration, sample_rate=sample_rate)

    expected_length = int(target_duration * sample_rate)
    assert result.shape == (expected_length,)


def test_extrapolator_handles_stereo_audio() -> None:
    """Extrapolator preserves stereo channel structure."""
    extrapolator = AudioDiffusionExtrapolator(device="cpu")

    sample_rate = 1000
    # Stereo audio: shape (2, samples)
    audio = np.random.randn(2, sample_rate)
    target_duration = 2.0

    result = extrapolator.extrapolate(audio, target_duration, sample_rate=sample_rate)

    expected_length = int(target_duration * sample_rate)
    assert result.shape == (2, expected_length)


def test_extrapolator_truncates_when_target_is_shorter() -> None:
    """Extrapolator truncates audio when target duration is shorter than input."""
    extrapolator = AudioDiffusionExtrapolator(device="cpu")

    sample_rate = 1000
    audio = np.ones(sample_rate * 2)  # 2 seconds
    target_duration = 1.0  # Want only 1 second

    result = extrapolator.extrapolate(audio, target_duration, sample_rate=sample_rate)

    expected_length = int(target_duration * sample_rate)
    assert result.shape == (expected_length,)
    # Check that we kept the beginning
    np.testing.assert_array_equal(result, audio[:expected_length])


def test_extrapolator_includes_original_audio_at_start() -> None:
    """Extrapolator includes the original input audio at the beginning."""
    extrapolator = AudioDiffusionExtrapolator(device="cpu")

    sample_rate = 1000
    audio = np.random.randn(sample_rate)
    target_duration = 3.0

    result = extrapolator.extrapolate(audio, target_duration, sample_rate=sample_rate)

    # Original audio should be at the start
    np.testing.assert_array_almost_equal(result[: len(audio)], audio)
