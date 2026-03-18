"""FFT-based spectrum analysis, STFT, mel filterbanks, MFCCs, and window functions."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array, _check_error


# ---------------------------------------------------------------------------
# FFT / Spectrum analysis
# ---------------------------------------------------------------------------

def lowpass_brickwall(signal: npt.ArrayLike, cutoff_hz: float, sample_rate: float) -> npt.NDArray[np.float64]:
    """
    Apply an FFT-based ideal (brickwall) lowpass filter.

    Zeroes all frequency bins above the cutoff frequency. Operates by
    copying the signal, applying the filter in-place, and returning the result.

    Args:
        signal: Input signal.
        cutoff_hz: Cutoff frequency in Hz.
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of the same length as the input.
    """
    signal = np.ascontiguousarray(signal, dtype=np.float64)
    out = signal.copy()
    out_ptr = ffi.cast("double *", out.ctypes.data)
    lib.MD_lowpass_brickwall(out_ptr, len(out), float(cutoff_hz), float(sample_rate))
    _check_error()
    return out

def magnitude_spectrum(signal: npt.ArrayLike) -> npt.NDArray[np.float64]:
    """
    Compute the magnitude spectrum of a real-valued signal.

    Returns:
        numpy array of length N/2 + 1 containing magnitudes.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_magnitude_spectrum(s_ptr, n, out_ptr)
    _check_error()
    return out


def power_spectral_density(signal: npt.ArrayLike) -> npt.NDArray[np.float64]:
    """
    Compute the power spectral density (PSD) of a signal.

    Returns:
        numpy array of length N/2 + 1 containing power values.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_power_spectral_density(s_ptr, n, out_ptr)
    _check_error()
    return out


def phase_spectrum(signal: npt.ArrayLike) -> npt.NDArray[np.float64]:
    """
    Compute the one-sided phase spectrum in radians.

    Returns:
        numpy array of length N/2 + 1 with phase in [-pi, pi].
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_phase_spectrum(s_ptr, n, out_ptr)
    _check_error()
    return out


def stft_num_frames(signal_len: int, n: int, hop: int) -> int:
    """Compute the number of STFT frames."""
    result = lib.MD_stft_num_frames(signal_len, n, hop)
    _check_error()
    return result


def stft(signal: npt.ArrayLike, n: int, hop: int) -> npt.NDArray[np.float64]:
    """
    Compute the Short-Time Fourier Transform (STFT).

    Args:
        signal: Input signal.
        n: FFT window size.
        hop: Hop size in samples.

    Returns:
        2D numpy array of shape (num_frames, n//2+1) containing magnitudes.
    """
    s_ptr, signal = _as_double_ptr(signal)
    signal_len = len(signal)
    num_frames = lib.MD_stft_num_frames(signal_len, n, hop)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_frames * num_bins)
    lib.MD_stft(s_ptr, signal_len, n, hop, out_ptr)
    _check_error()
    return out.reshape(num_frames, num_bins)


def mel_filterbank(n: int, sample_rate: float, num_mels: int = 26, min_freq_hz: float = 0.0, max_freq_hz: float | None = None) -> npt.NDArray[np.float64]:
    """
    Build a mel-spaced triangular filterbank matrix.

    Args:
        n: FFT size.
        sample_rate: Sampling rate in Hz.
        num_mels: Number of mel filters.
        min_freq_hz: Lower frequency bound.
        max_freq_hz: Upper frequency bound (defaults to sample_rate/2).

    Returns:
        2D numpy array of shape (num_mels, n//2+1).
    """
    if max_freq_hz is None:
        max_freq_hz = sample_rate / 2.0
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_mels * num_bins)
    lib.MD_mel_filterbank(n, sample_rate, num_mels, min_freq_hz, max_freq_hz, out_ptr)
    _check_error()
    return out.reshape(num_mels, num_bins)


def mel_energies(signal: npt.ArrayLike, sample_rate: float, num_mels: int = 26, min_freq_hz: float = 0.0, max_freq_hz: float | None = None) -> npt.NDArray[np.float64]:
    """
    Compute mel-band energies from a single frame.

    Returns:
        numpy array of length num_mels.
    """
    if max_freq_hz is None:
        max_freq_hz = sample_rate / 2.0
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(num_mels)
    lib.MD_mel_energies(s_ptr, n, sample_rate, num_mels, min_freq_hz, max_freq_hz, out_ptr)
    _check_error()
    return out


def mfcc(signal: npt.ArrayLike, sample_rate: float, num_mels: int = 26, num_coeffs: int = 13,
         min_freq_hz: float = 0.0, max_freq_hz: float | None = None) -> npt.NDArray[np.float64]:
    """
    Compute MFCCs from a single frame.

    Args:
        signal: Input frame.
        sample_rate: Sampling rate in Hz.
        num_mels: Number of mel bands.
        num_coeffs: Number of cepstral coefficients to output.
        min_freq_hz: Lower frequency bound.
        max_freq_hz: Upper frequency bound (defaults to sample_rate/2).

    Returns:
        numpy array of length num_coeffs.
    """
    if max_freq_hz is None:
        max_freq_hz = sample_rate / 2.0
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(num_coeffs)
    lib.MD_mfcc(s_ptr, n, sample_rate, num_mels, num_coeffs,
                min_freq_hz, max_freq_hz, out_ptr)
    _check_error()
    return out


# ---------------------------------------------------------------------------
# Window generation
# ---------------------------------------------------------------------------

def hann_window(n: int) -> npt.NDArray[np.float64]:
    """Generate a Hanning (Hann) window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Hann_Win(out_ptr, n)
    _check_error()
    return out


def hamming_window(n: int) -> npt.NDArray[np.float64]:
    """Generate a Hamming window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Hamming_Win(out_ptr, n)
    _check_error()
    return out


def blackman_window(n: int) -> npt.NDArray[np.float64]:
    """Generate a Blackman window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Blackman_Win(out_ptr, n)
    _check_error()
    return out


def rect_window(n: int) -> npt.NDArray[np.float64]:
    """Generate a rectangular window of length n (all ones)."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Rect_Win(out_ptr, n)
    _check_error()
    return out


def kaiser_window(n: int, beta: float) -> npt.NDArray[np.float64]:
    """
    Generate a Kaiser window of length n with shape parameter beta.

    Unlike other window functions, Kaiser windows require a beta parameter
    that controls the trade-off between main-lobe width and side-lobe level.
    Higher beta gives lower sidelobes but a wider main lobe.

    Args:
        n: Window length.
        beta: Shape parameter (typical values: 5-14).

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Kaiser_Win(out_ptr, n, float(beta))
    _check_error()
    return out
