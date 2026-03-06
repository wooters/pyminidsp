"""Signal measurement, analysis, and scaling functions."""

import numpy as np

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array

# ---------------------------------------------------------------------------
# Signal measurement
# ---------------------------------------------------------------------------

def dot(a, b):
    """Compute the dot product of two vectors."""
    a_ptr, a = _as_double_ptr(a)
    b_ptr, b = _as_double_ptr(b)
    n = min(len(a), len(b))
    return lib.MD_dot(a_ptr, b_ptr, n)


def entropy(a, clip=False):
    """Compute the normalized entropy of a distribution."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_entropy(a_ptr, len(a), clip)


def energy(a):
    """Compute signal energy: sum of squared samples."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_energy(a_ptr, len(a))


def power(a):
    """Compute signal power: energy / N."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_power(a_ptr, len(a))


def power_db(a):
    """Compute signal power in decibels."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_power_db(a_ptr, len(a))


# ---------------------------------------------------------------------------
# Signal analysis
# ---------------------------------------------------------------------------

def rms(a):
    """Compute the root mean square (RMS) of a signal."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_rms(a_ptr, len(a))


def zero_crossing_rate(a):
    """Compute the zero-crossing rate of a signal."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_zero_crossing_rate(a_ptr, len(a))


def autocorrelation(a, max_lag):
    """
    Compute the normalised autocorrelation of a signal.

    Args:
        a: Input signal.
        max_lag: Number of lag values to compute.

    Returns:
        numpy array of autocorrelation values, length max_lag.
    """
    a_ptr, a = _as_double_ptr(a)
    out, out_ptr = _new_double_array(max_lag)
    lib.MD_autocorrelation(a_ptr, len(a), out_ptr, max_lag)
    return out


def peak_detect(a, threshold=0.0, min_distance=1):
    """
    Detect peaks (local maxima) in a signal.

    Args:
        a: Input signal.
        threshold: Minimum value for a peak.
        min_distance: Minimum index gap between peaks.

    Returns:
        numpy array of peak indices.
    """
    a_ptr, a = _as_double_ptr(a)
    n = len(a)
    peaks = np.zeros(n, dtype=np.uint32)
    num_peaks = ffi.new("unsigned *")
    lib.MD_peak_detect(
        a_ptr, n, threshold, min_distance,
        ffi.cast("unsigned *", peaks.ctypes.data), num_peaks,
    )
    return peaks[: num_peaks[0]].copy()


def f0_autocorrelation(signal, sample_rate, min_freq_hz=80.0, max_freq_hz=400.0):
    """Estimate F0 using autocorrelation."""
    s_ptr, signal = _as_double_ptr(signal)
    return lib.MD_f0_autocorrelation(s_ptr, len(signal), sample_rate, min_freq_hz, max_freq_hz)


def f0_fft(signal, sample_rate, min_freq_hz=80.0, max_freq_hz=400.0):
    """Estimate F0 using FFT peak picking."""
    s_ptr, signal = _as_double_ptr(signal)
    return lib.MD_f0_fft(s_ptr, len(signal), sample_rate, min_freq_hz, max_freq_hz)


def mix(a, b, w_a=0.5, w_b=0.5):
    """
    Mix (weighted sum) two signals.

    Args:
        a, b: Input signals of the same length.
        w_a, w_b: Weights for signals a and b.

    Returns:
        numpy array of the mixed signal.
    """
    a_ptr, a = _as_double_ptr(a)
    b_ptr, b = _as_double_ptr(b)
    n = min(len(a), len(b))
    out, out_ptr = _new_double_array(n)
    lib.MD_mix(a_ptr, b_ptr, out_ptr, n, w_a, w_b)
    return out


# ---------------------------------------------------------------------------
# Signal scaling
# ---------------------------------------------------------------------------

def scale(value, oldmin, oldmax, newmin, newmax):
    """Map a single value from one range to another."""
    return lib.MD_scale(value, oldmin, oldmax, newmin, newmax)


def scale_vec(a, oldmin, oldmax, newmin, newmax):
    """Map every element of a vector from one range to another."""
    a_ptr, a_arr = _as_double_ptr(a)
    n = len(a_arr)
    out, out_ptr = _new_double_array(n)
    # MD_scale_vec takes non-const input pointer
    in_copy = np.array(a_arr, dtype=np.float64, copy=True)
    in_ptr = ffi.cast("double *", in_copy.ctypes.data)
    lib.MD_scale_vec(in_ptr, out_ptr, n, oldmin, oldmax, newmin, newmax)
    return out


def fit_within_range(a, newmin, newmax):
    """Fit values within [newmin, newmax]."""
    a_arr = np.ascontiguousarray(a, dtype=np.float64)
    n = len(a_arr)
    in_copy = np.array(a_arr, copy=True)
    in_ptr = ffi.cast("double *", in_copy.ctypes.data)
    out, out_ptr = _new_double_array(n)
    lib.MD_fit_within_range(in_ptr, out_ptr, n, newmin, newmax)
    return out


def adjust_dblevel(signal, dblevel):
    """Automatic Gain Control: scale signal to target dB level, clip to [-1, 1]."""
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_adjust_dblevel(s_ptr, out_ptr, n, dblevel)
    return out
