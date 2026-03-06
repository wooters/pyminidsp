"""Generalized Cross-Correlation (GCC) delay estimation."""

import numpy as np

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array, GCC_PHAT


def get_delay(sig_a, sig_b, margin, weighting=GCC_PHAT):
    """
    Estimate the delay between two signals using GCC.

    Args:
        sig_a: First signal.
        sig_b: Second signal.
        margin: Search +/- this many samples around zero-lag.
        weighting: GCC_SIMP or GCC_PHAT.

    Returns:
        (delay, entropy) tuple. Delay in samples (positive = sig_b lags sig_a).
    """
    a_ptr, sig_a = _as_double_ptr(sig_a)
    b_ptr, sig_b = _as_double_ptr(sig_b)
    n = min(len(sig_a), len(sig_b))
    ent = ffi.new("double *")
    delay = lib.MD_get_delay(a_ptr, b_ptr, n, ent, margin, weighting)
    return delay, ent[0]


def get_multiple_delays(signals, margin, weighting=GCC_PHAT):
    """
    Estimate delays between a reference signal and M-1 other signals.

    Args:
        signals: List of numpy arrays (signals[0] is reference).
        margin: Search window in samples.
        weighting: GCC_SIMP or GCC_PHAT.

    Returns:
        numpy array of M-1 delay values.
    """
    m = len(signals)
    n = min(len(s) for s in signals)
    ptrs = []
    kept = []  # prevent GC
    for s in signals:
        p, arr = _as_double_ptr(s)
        ptrs.append(p)
        kept.append(arr)
    sigs_arr = ffi.new("const double *[]", ptrs)
    delays = np.zeros(m - 1, dtype=np.int32)
    lib.MD_get_multiple_delays(
        sigs_arr, m, n, margin, weighting,
        ffi.cast("int *", delays.ctypes.data),
    )
    return delays


def gcc(sig_a, sig_b, weighting=GCC_PHAT):
    """
    Compute the full generalized cross-correlation between two signals.

    Args:
        sig_a: First signal.
        sig_b: Second signal.
        weighting: GCC_SIMP or GCC_PHAT.

    Returns:
        numpy array of N doubles (zero-lag at index ceil(N/2)).
    """
    a_ptr, sig_a = _as_double_ptr(sig_a)
    b_ptr, sig_b = _as_double_ptr(sig_b)
    n = min(len(sig_a), len(sig_b))
    out, out_ptr = _new_double_array(n)
    lib.MD_gcc(a_ptr, b_ptr, n, out_ptr, weighting)
    return out
