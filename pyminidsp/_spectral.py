"""FFT-based spectrum analysis, STFT, mel filterbanks, MFCCs, and window functions."""

from pyminidsp._minidsp_cffi import lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array


# ---------------------------------------------------------------------------
# FFT / Spectrum analysis
# ---------------------------------------------------------------------------

def magnitude_spectrum(signal):
    """
    Compute the magnitude spectrum of a real-valued signal.

    Returns:
        numpy array of length N/2 + 1 containing |X(k)|.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_magnitude_spectrum(s_ptr, n, out_ptr)
    return out


def power_spectral_density(signal):
    """
    Compute the power spectral density (PSD) of a signal.

    Returns:
        numpy array of length N/2 + 1 containing |X(k)|^2 / N.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_power_spectral_density(s_ptr, n, out_ptr)
    return out


def phase_spectrum(signal):
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
    return out


def stft_num_frames(signal_len, n, hop):
    """Compute the number of STFT frames."""
    return lib.MD_stft_num_frames(signal_len, n, hop)


def stft(signal, n, hop):
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
    return out.reshape(num_frames, num_bins)


def mel_filterbank(n, sample_rate, num_mels=26, min_freq_hz=0.0, max_freq_hz=None):
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
    return out.reshape(num_mels, num_bins)


def mel_energies(signal, sample_rate, num_mels=26, min_freq_hz=0.0, max_freq_hz=None):
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
    return out


def mfcc(signal, sample_rate, num_mels=26, num_coeffs=13,
         min_freq_hz=0.0, max_freq_hz=None):
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
    return out


# ---------------------------------------------------------------------------
# Window generation
# ---------------------------------------------------------------------------

def hann_window(n):
    """Generate a Hanning (Hann) window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Hann_Win(out_ptr, n)
    return out


def hamming_window(n):
    """Generate a Hamming window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Hamming_Win(out_ptr, n)
    return out


def blackman_window(n):
    """Generate a Blackman window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Blackman_Win(out_ptr, n)
    return out


def rect_window(n):
    """Generate a rectangular window of length n (all ones)."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Rect_Win(out_ptr, n)
    return out
