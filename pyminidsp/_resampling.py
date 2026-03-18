"""Polyphase sinc resampling (sample rate conversion)."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from pyminidsp._minidsp_cffi import lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array, _check_error


def resample_output_len(input_len: int, in_rate: float, out_rate: float) -> int:
    """Compute the number of output samples for a given resampling operation."""
    result = lib.MD_resample_output_len(input_len, float(in_rate), float(out_rate))
    _check_error()
    return result


def resample(signal: npt.ArrayLike, in_rate: float, out_rate: float, num_zero_crossings: int = 13, kaiser_beta: float = 5.0) -> npt.NDArray[np.float64]:
    """
    Resample a signal using a polyphase sinc resampler with Kaiser-windowed
    anti-aliasing filter.

    Args:
        signal: Input signal.
        in_rate: Input sample rate in Hz.
        out_rate: Output sample rate in Hz.
        num_zero_crossings: Number of zero crossings in the sinc kernel (default 13).
        kaiser_beta: Kaiser window shape parameter (default 5.0).

    Returns:
        numpy array of resampled signal.
    """
    s_ptr, signal = _as_double_ptr(signal)
    input_len = len(signal)
    max_output_len = lib.MD_resample_output_len(input_len, float(in_rate), float(out_rate))
    _check_error()
    out, out_ptr = _new_double_array(max_output_len)
    actual_len = lib.MD_resample(
        s_ptr, input_len, out_ptr, max_output_len,
        float(in_rate), float(out_rate),
        int(num_zero_crossings), float(kaiser_beta),
    )
    _check_error()
    return out[:actual_len]
