"""FIR filters, convolution, and biquad (IIR) filtering."""

import numpy as np

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array


# ---------------------------------------------------------------------------
# FIR filters / convolution
# ---------------------------------------------------------------------------

def convolution_num_samples(signal_len, kernel_len):
    """Compute the output length of a full linear convolution."""
    return lib.MD_convolution_num_samples(signal_len, kernel_len)


def convolution_time(signal, kernel):
    """
    Time-domain full linear convolution.

    Returns:
        numpy array of length signal_len + kernel_len - 1.
    """
    s_ptr, signal = _as_double_ptr(signal)
    k_ptr, kernel = _as_double_ptr(kernel)
    out_len = len(signal) + len(kernel) - 1
    out, out_ptr = _new_double_array(out_len)
    lib.MD_convolution_time(s_ptr, len(signal), k_ptr, len(kernel), out_ptr)
    return out


def moving_average(signal, window_len):
    """
    Causal moving-average FIR filter.

    Returns:
        numpy array of the same length as the input.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_moving_average(s_ptr, n, window_len, out_ptr)
    return out


def fir_filter(signal, coeffs):
    """
    Apply a causal FIR filter with arbitrary coefficients.

    Returns:
        numpy array of the same length as the input.
    """
    s_ptr, signal = _as_double_ptr(signal)
    c_ptr, coeffs = _as_double_ptr(coeffs)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_fir_filter(s_ptr, n, c_ptr, len(coeffs), out_ptr)
    return out


def convolution_fft_ola(signal, kernel):
    """
    Full linear convolution using FFT overlap-add.

    Returns:
        numpy array of length signal_len + kernel_len - 1.
    """
    s_ptr, signal = _as_double_ptr(signal)
    k_ptr, kernel = _as_double_ptr(kernel)
    out_len = len(signal) + len(kernel) - 1
    out, out_ptr = _new_double_array(out_len)
    lib.MD_convolution_fft_ola(s_ptr, len(signal), k_ptr, len(kernel), out_ptr)
    return out


# ---------------------------------------------------------------------------
# Biquad filter
# ---------------------------------------------------------------------------

class BiquadFilter:
    """
    Biquad (second-order IIR) filter.

    Supports low-pass, high-pass, band-pass, notch, peaking EQ,
    low shelf, and high shelf filter types.

    Example:
        >>> filt = BiquadFilter(LPF, freq=1000.0, sample_rate=44100.0)
        >>> for sample in signal:
        ...     output = filt.process(sample)
    """

    def __init__(self, filter_type, freq, sample_rate, db_gain=0.0, bandwidth=1.0):
        """
        Create a new biquad filter.

        Args:
            filter_type: One of LPF, HPF, BPF, NOTCH, PEQ, LSH, HSH.
            freq: Centre/corner frequency in Hz.
            sample_rate: Sampling rate in Hz.
            db_gain: Gain in dB (only for PEQ, LSH, HSH).
            bandwidth: Bandwidth in octaves.
        """
        self._ptr = lib.BiQuad_new(filter_type, db_gain, freq, sample_rate, bandwidth)
        if self._ptr == ffi.NULL:
            raise MemoryError("Failed to allocate biquad filter")

    def __del__(self):
        if hasattr(self, "_ptr") and self._ptr != ffi.NULL:
            lib.free(self._ptr)
            self._ptr = ffi.NULL

    def process(self, sample):
        """Process a single sample through the filter."""
        return lib.BiQuad(sample, self._ptr)

    def process_array(self, signal):
        """
        Process an entire signal through the filter.

        Args:
            signal: Input numpy array.

        Returns:
            Filtered numpy array.
        """
        signal = np.asarray(signal, dtype=np.float64)
        out = np.empty_like(signal)
        for i in range(len(signal)):
            out[i] = lib.BiQuad(signal[i], self._ptr)
        return out
