"""Concrete implementations of audio interpolation models."""

from audio_diffusion_pytorch import VInpainter
import numpy as np
import torch


class AudioDiffusionInterpolator:
    """Audio interpolator using audio-diffusion-pytorch's VInpainter.

    This implementation uses a variational inpainting approach with diffusion
    models to fill gaps between audio segments smoothly.
    """

    def __init__(self, device: str | None = None):
        """Initialize the interpolator.

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

        # TODO: Load pretrained weights or train model
        # NOTE: VInpainter instantiation commented out until we have model weights
        # self._model = VInpainter(
        #     # Model configuration will go here
        # ).to(self.device)
        self._model: VInpainter | None = None

    def interpolate(
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
        """
        # Convert to torch tensors
        # float<samples> or float<channels, samples>
        audio1_tensor = torch.from_numpy(audio1).float().to(self.device)
        # float<samples> or float<channels, samples>
        audio2_tensor = torch.from_numpy(audio2).float().to(self.device)

        # Calculate gap size in samples
        gap_samples = int(gap_duration * sample_rate)

        # Ensure audio is the right shape (add batch dimension if needed)
        if audio1_tensor.ndim == 1:
            # float<1, samples>
            audio1_tensor = audio1_tensor.unsqueeze(0)
            # float<1, samples>
            audio2_tensor = audio2_tensor.unsqueeze(0)
            squeeze_output = True
        else:
            squeeze_output = False

        # Create full audio with gap (filled with zeros initially)
        # float<channels, total_samples>
        total_samples = audio1_tensor.shape[1] + gap_samples + audio2_tensor.shape[1]
        full_audio = torch.zeros(
            audio1_tensor.shape[0], total_samples, device=self.device
        )
        full_audio[:, : audio1_tensor.shape[1]] = audio1_tensor
        full_audio[:, -audio2_tensor.shape[1] :] = audio2_tensor

        # Create mask (1 = interpolate this region, 0 = keep original)
        # float<channels, total_samples>
        mask = torch.zeros_like(full_audio)
        mask[:, audio1_tensor.shape[1] : -audio2_tensor.shape[1]] = 1.0

        # TODO: Perform interpolation with the model
        # This is a placeholder - actual implementation depends on model architecture
        # interpolated = self._model(full_audio, mask)

        # For now, return a simple crossfade as placeholder
        # This will be replaced with actual diffusion interpolation
        interpolated = self._simple_crossfade(audio1_tensor, audio2_tensor, gap_samples)

        # Convert back to numpy
        result = interpolated.cpu().numpy()

        if squeeze_output:
            result = result.squeeze(0)

        return result

    def _simple_crossfade(
        self, audio1: torch.Tensor, audio2: torch.Tensor, gap_samples: int
    ) -> torch.Tensor:
        """Simple crossfade placeholder until diffusion model is ready.

        Args:
            audio1: First audio segment (shape: [channels, samples])
            audio2: Second audio segment (shape: [channels, samples])
            gap_samples: Number of samples for the gap

        Returns:
            Concatenated audio with crossfade
        """
        # TODO: Implement actual crossfade with gap_samples
        # For now, just concatenate
        # float<channels, total_samples>
        result = torch.cat([audio1, audio2], dim=1)

        return result
