"""Signal generators: sine, noise, impulse, chirps, and spectrogram text."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array, _check_error


def sine_wave(n: int, amplitude: float = 1.0, freq: float = 440.0, sample_rate: float = 44100.0) -> npt.NDArray[np.float64]:
    """
    Generate a sine wave.

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        freq: Frequency in Hz.
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_sine_wave(out_ptr, n, amplitude, freq, sample_rate)
    _check_error()
    return out


def white_noise(n: int, amplitude: float = 1.0, seed: int = 42) -> npt.NDArray[np.float64]:
    """
    Generate Gaussian white noise.

    Args:
        n: Number of samples.
        amplitude: Standard deviation.
        seed: Random seed for reproducibility.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_white_noise(out_ptr, n, amplitude, seed)
    _check_error()
    return out


def impulse(n: int, amplitude: float = 1.0, position: int = 0) -> npt.NDArray[np.float64]:
    """
    Generate a discrete impulse (Kronecker delta).

    Args:
        n: Number of samples.
        amplitude: Spike amplitude.
        position: Sample index of the spike.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_impulse(out_ptr, n, amplitude, position)
    _check_error()
    return out


def chirp_linear(n: int, amplitude: float = 1.0, f_start: float = 200.0, f_end: float = 4000.0, sample_rate: float = 16000.0) -> npt.NDArray[np.float64]:
    """
    Generate a linear chirp (swept sine).

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        f_start: Starting frequency in Hz.
        f_end: Ending frequency in Hz.
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_chirp_linear(out_ptr, n, amplitude, f_start, f_end, sample_rate)
    _check_error()
    return out


def chirp_log(n: int, amplitude: float = 1.0, f_start: float = 20.0, f_end: float = 20000.0, sample_rate: float = 44100.0) -> npt.NDArray[np.float64]:
    """
    Generate a logarithmic chirp.

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        f_start: Starting frequency in Hz (must be > 0).
        f_end: Ending frequency in Hz (must be > 0, != f_start).
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_chirp_log(out_ptr, n, amplitude, f_start, f_end, sample_rate)
    _check_error()
    return out


def square_wave(n: int, amplitude: float = 1.0, freq: float = 440.0, sample_rate: float = 44100.0) -> npt.NDArray[np.float64]:
    """Generate a square wave."""
    out, out_ptr = _new_double_array(n)
    lib.MD_square_wave(out_ptr, n, amplitude, freq, sample_rate)
    _check_error()
    return out


def sawtooth_wave(n: int, amplitude: float = 1.0, freq: float = 440.0, sample_rate: float = 44100.0) -> npt.NDArray[np.float64]:
    """Generate a sawtooth wave."""
    out, out_ptr = _new_double_array(n)
    lib.MD_sawtooth_wave(out_ptr, n, amplitude, freq, sample_rate)
    _check_error()
    return out


def shepard_tone(n: int, amplitude: float = 0.8, base_freq: float = 440.0, sample_rate: float = 44100.0,
                 rate_octaves_per_sec: float = 0.5, num_octaves: int = 8) -> npt.NDArray[np.float64]:
    """
    Generate a Shepard tone (auditory illusion of endlessly rising/falling pitch).

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        base_freq: Centre frequency of the Gaussian envelope in Hz.
        sample_rate: Sampling rate in Hz.
        rate_octaves_per_sec: Glissando rate (positive=rising, negative=falling).
        num_octaves: Number of audible octave layers.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_shepard_tone(out_ptr, n, amplitude, base_freq, sample_rate,
                        rate_octaves_per_sec, num_octaves)
    _check_error()
    return out


# ---------------------------------------------------------------------------
# Spectrogram text
# ---------------------------------------------------------------------------

def spectrogram_text(text: str, freq_lo: float = 200.0, freq_hi: float = 7500.0,
                     duration_sec: float = 2.0, sample_rate: float = 16000.0) -> npt.NDArray[np.float64]:
    """
    Synthesise audio that displays readable text in a spectrogram.

    Args:
        text: ASCII string to render.
        freq_lo: Lowest frequency in Hz.
        freq_hi: Highest frequency in Hz.
        duration_sec: Total duration in seconds.
        sample_rate: Sample rate in Hz.

    Returns:
        numpy array of audio samples.
    """
    max_len = int(duration_sec * sample_rate) + 1024
    out, out_ptr = _new_double_array(max_len)
    text_bytes = text.encode("ascii")
    n_written = lib.MD_spectrogram_text(out_ptr, max_len, text_bytes,
                                         freq_lo, freq_hi,
                                         duration_sec, sample_rate)
    _check_error()
    return out[:n_written].copy()
