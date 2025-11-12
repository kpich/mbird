"""Concrete implementations of audio expansion models."""

from audio_diffusion_pytorch import DiffusionModel
import numpy as np
import torch


class AudioDiffusionExpander:
    """Audio expander using audio-diffusion-pytorch for extrapolation.

    This implementation uses diffusion models to expand short audio clips
    to longer durations by plausibly continuing the audio.
    """

    def __init__(self, device: str | None = None):
        """Initialize the expander.

        Args:
            device: Device to run inference on. If None, auto-detects
                   (prefers MPS on Mac, CUDA on GPU systems, falls back to CPU)
        """
        if device is None:
            if torch.backends.mps.is_available():
                device = "mps"
            elif torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"

        self.device = torch.device(device)
        self._model: DiffusionModel | None = None

    def _ensure_model_loaded(self) -> None:
        """Lazy load the model on first use."""
        if self._model is None:
            # NOTE: DiffusionModel will need to be instantiated with a trained model
            # For now, this is a placeholder that will require model weights
            # TODO: Load pretrained weights or train model for expansion
            self._model = DiffusionModel(
                # Model configuration will go here
                # This is intentionally incomplete until we have trained weights
            )
            self._model = self._model.to(self.device)

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
            Expanded audio of target_duration length
        """
        self._ensure_model_loaded()

        # Convert to torch tensor
        # float<samples> or float<channels, samples>
        audio_tensor = torch.from_numpy(audio).float().to(self.device)

        # Calculate target samples
        target_samples = int(target_duration * sample_rate)
        current_samples = audio_tensor.shape[-1]

        if target_samples <= current_samples:
            # If target is shorter or equal, just truncate
            if audio_tensor.ndim == 1:
                return audio[:target_samples]
            else:
                return audio[:, :target_samples]

        # Ensure audio is the right shape (add batch dimension if needed)
        if audio_tensor.ndim == 1:
            # float<1, samples>
            audio_tensor = audio_tensor.unsqueeze(0)
            squeeze_output = True
        else:
            squeeze_output = False

        # Calculate how many samples to generate
        samples_to_generate = target_samples - current_samples

        # TODO: Perform expansion with the model
        # This is a placeholder - actual implementation depends on model architecture
        # Options:
        # 1. Autoregressively generate continuation
        # 2. Generate entire target length conditioned on input
        # 3. Use inpainting with partial conditioning

        # For now, return a simple repeat/fade as placeholder
        # This will be replaced with actual diffusion expansion
        expanded = self._simple_repeat_fade(audio_tensor, samples_to_generate)

        # Convert back to numpy
        result = expanded.cpu().numpy()

        if squeeze_output:
            result = result.squeeze(0)

        return result

    def _simple_repeat_fade(
        self, audio: torch.Tensor, samples_to_generate: int
    ) -> torch.Tensor:
        """Simple repeat and fade placeholder until diffusion model is ready.

        Args:
            audio: Input audio segment (shape: [channels, samples])
            samples_to_generate: Number of samples to add

        Returns:
            Expanded audio
        """
        # Take the last portion and repeat with fade
        repeat_length = min(samples_to_generate, audio.shape[1])
        # float<channels, repeat_length>
        tail = audio[:, -repeat_length:]

        # Create fade out
        # float<repeat_length>
        fade = torch.linspace(1.0, 0.0, repeat_length, device=self.device)
        # float<channels, repeat_length>
        faded_tail = tail * fade

        # Concatenate
        # float<channels, total_samples>
        result = torch.cat([audio, faded_tail], dim=1)

        # If we still need more samples, pad with silence
        if result.shape[1] < audio.shape[1] + samples_to_generate:
            padding_needed = audio.shape[1] + samples_to_generate - result.shape[1]
            # float<channels, padding_needed>
            padding = torch.zeros(
                audio.shape[0], padding_needed, device=self.device, dtype=audio.dtype
            )
            result = torch.cat([result, padding], dim=1)

        return result
