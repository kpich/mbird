from pathlib import Path
import wave

import pytest

from mbird_audiogen import MbirdGenerator
from mbird_data import MbirdNode


def test_generate_node_audio_creates_wav_file(tmp_path: Path):
    """Unit test: verify audio file is created with correct format."""
    generator = MbirdGenerator()
    node = MbirdNode(id="test_node", length=0.5)  # 0.5 second audio
    output_path = tmp_path / "test.wav"

    generator.generate_node_audio(node, output_path)

    # Verify file was created
    assert output_path.exists()

    # Verify WAV format
    with wave.open(str(output_path), "rb") as wav_file:
        assert wav_file.getnchannels() == 1  # Mono
        assert wav_file.getsampwidth() == 2  # 16-bit (2 bytes)
        assert wav_file.getframerate() == 44100  # Sample rate

        # Verify duration (approximately 0.5 seconds)
        n_frames = wav_file.getnframes()
        duration = n_frames / 44100
        assert duration == pytest.approx(0.5, abs=0.01)


def test_generate_node_audio_with_different_lengths(tmp_path: Path):
    """Unit test: verify different durations produce correct file sizes."""
    generator = MbirdGenerator()

    short_node = MbirdNode(id="short", length=0.1)
    long_node = MbirdNode(id="long", length=2.0)

    short_path = tmp_path / "short.wav"
    long_path = tmp_path / "long.wav"

    generator.generate_node_audio(short_node, short_path)
    generator.generate_node_audio(long_node, long_path)

    # Verify both files exist
    assert short_path.exists()
    assert long_path.exists()

    # Verify longer audio has more frames
    with wave.open(str(short_path), "rb") as short_wav:
        short_frames = short_wav.getnframes()

    with wave.open(str(long_path), "rb") as long_wav:
        long_frames = long_wav.getnframes()

    assert long_frames > short_frames
    assert long_frames / short_frames > 15  # ~20x longer


def test_generate_node_audio_skips_invalid_length(tmp_path: Path):
    """Unit test: verify no file is created for invalid lengths."""
    generator = MbirdGenerator()

    # Test None length
    none_node = MbirdNode(id="none", length=None, children=[])
    none_path = tmp_path / "none.wav"
    generator.generate_node_audio(none_node, none_path)
    assert not none_path.exists()

    # Test zero length
    zero_node = MbirdNode(id="zero", length=0.0)
    zero_path = tmp_path / "zero.wav"
    generator.generate_node_audio(zero_node, zero_path)
    assert not zero_path.exists()
