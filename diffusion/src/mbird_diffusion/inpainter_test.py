"""Tests for audio inpainting implementations."""

import numpy as np

from mbird_diffusion.inpainter import AudioDiffusionInpainter


def test_inpainter_returns_audio_with_correct_total_length() -> None:
    """Inpainter concatenates audio1, gap, and audio2 with correct total length."""
    inpainter = AudioDiffusionInpainter(device="cpu")

    # Create simple test audio (1 second each at 1000 Hz for fast testing)
    sample_rate = 1000
    audio1 = np.sin(2 * np.pi * 440 * np.linspace(0, 1, sample_rate))
    audio2 = np.sin(2 * np.pi * 880 * np.linspace(0, 1, sample_rate))
    gap_duration = 0.5

    result = inpainter.inpaint(audio1, audio2, gap_duration, sample_rate=sample_rate)

    expected_length = len(audio1) + int(gap_duration * sample_rate) + len(audio2)
    assert result.shape == (expected_length,)


def test_inpainter_handles_stereo_audio() -> None:
    """Inpainter preserves stereo channel structure."""
    inpainter = AudioDiffusionInpainter(device="cpu")

    sample_rate = 1000
    # Stereo audio: shape (2, samples)
    audio1 = np.random.randn(2, sample_rate)
    audio2 = np.random.randn(2, sample_rate)
    gap_duration = 0.5

    result = inpainter.inpaint(audio1, audio2, gap_duration, sample_rate=sample_rate)

    expected_length = (
        audio1.shape[1] + int(gap_duration * sample_rate) + audio2.shape[1]
    )
    assert result.shape == (2, expected_length)


def test_inpainter_preserves_input_audio_segments() -> None:
    """Inpainter keeps original audio1 at start and audio2 at end."""
    inpainter = AudioDiffusionInpainter(device="cpu")

    sample_rate = 1000
    audio1 = np.ones(sample_rate) * 0.5
    audio2 = np.ones(sample_rate) * -0.5
    gap_duration = 0.5

    result = inpainter.inpaint(audio1, audio2, gap_duration, sample_rate=sample_rate)

    # Check that audio1 is at the beginning
    np.testing.assert_array_almost_equal(result[: len(audio1)], audio1)
    # Check that audio2 is at the end
    np.testing.assert_array_almost_equal(result[-len(audio2) :], audio2)
