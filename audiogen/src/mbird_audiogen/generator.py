from pathlib import Path
import random
import wave

import numpy as np

from mbird_data import MbirdNode


class MbirdGenerator:
    """Generates audio for mbird nodes."""

    def generate_node_audio(self, node: MbirdNode, output_path: Path) -> None:
        """Generate sinusoid audio file for a node.

        Args:
            node: The node to generate audio for
            output_path: Path where the WAV file should be written
        """
        if node.length is None or node.length <= 0:
            return

        # Random frequency between 200 and 1000 Hz
        frequency = random.uniform(200, 1000)
        sample_rate = 44100
        duration = node.length

        # Generate sinusoid
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        audio = np.sin(2 * np.pi * frequency * t)

        # Convert to int16 for WAV
        audio_int16 = (audio * 32767).astype(np.int16)

        # Write WAV file
        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

    def concatenate_leaf_nodes(self, clip_paths: list[Path], output_path: Path) -> None:
        """Concatenate WAV files from leaf nodes into a single output file.

        Args:
            clip_paths: List of paths to WAV files in desired order
            output_path: Path where the concatenated WAV file should be written
        """
        if not clip_paths:
            return

        all_audio = []
        sample_rate = None

        for clip_path in clip_paths:
            if not clip_path.exists():
                continue

            with wave.open(str(clip_path), "rb") as wav_file:
                # Get audio parameters
                if sample_rate is None:
                    sample_rate = wav_file.getframerate()

                # Read audio data
                frames = wav_file.readframes(wav_file.getnframes())
                audio_data = np.frombuffer(frames, dtype=np.int16)
                all_audio.append(audio_data)

        if not all_audio or sample_rate is None:
            return

        # Concatenate all audio
        concatenated = np.concatenate(all_audio)

        # Write concatenated WAV file
        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(concatenated.tobytes())
