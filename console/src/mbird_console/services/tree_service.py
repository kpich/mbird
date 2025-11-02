import random
from typing import Any
import wave

import numpy as np

from mbird_data import MbirdData, MbirdNode


class TreeService:
    """Manages tree operations and transformations."""

    @staticmethod
    def get_tree(data: MbirdData) -> dict[str, Any]:
        """Get tree data as dictionary."""
        if data.root is None:
            raise ValueError("No root node in project data")
        return data.root.model_dump()

    @staticmethod
    def update_tree(tree_data: dict[str, Any]) -> MbirdData:
        """Update tree with validation and length transfer."""
        tree_data = TreeService.transfer_length_to_leaves(tree_data)
        root = MbirdNode(**tree_data)
        return MbirdData(root=root)

    @staticmethod
    def regenerate(data: MbirdData) -> MbirdData:
        """Run generate() to set is_stale=False for all nodes."""
        if data.root is None:
            raise ValueError("No root node in project data")
        TreeService.generate(data.root, data)
        return data

    @staticmethod
    def generate(node: MbirdNode, data: MbirdData) -> None:
        """Recursively set is_stale=False and generate audio for stale leaf nodes."""
        if node.is_stale and not node.children:
            # Leaf node that is stale - generate audio
            TreeService._generate_audio(node, data)

        node.is_stale = False
        for child in node.children:
            TreeService.generate(child, data)

    @staticmethod
    def _generate_audio(node: MbirdNode, data: MbirdData) -> None:
        """Generate sinusoid audio file for a node."""
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

        # Get clip path from data
        clip_path = data.get_clip_path(node.id)

        # Write WAV file
        with wave.open(str(clip_path), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

        # Set sound_file reference
        node.sound_file = f"{node.id}.wav"

    @staticmethod
    def transfer_length_to_leaves(tree_data: dict[str, Any]) -> dict[str, Any]:
        """Transfer length from non-leaf to children (leaf-only constraint)."""
        if not tree_data.get("children"):
            return tree_data

        parent_length = tree_data.get("length")
        children = tree_data["children"]

        if parent_length is not None and children:
            for child in children:
                child["length"] = parent_length
            tree_data["length"] = None

        tree_data["children"] = [
            TreeService.transfer_length_to_leaves(child) for child in children
        ]

        return tree_data
