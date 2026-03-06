"""Simple audio effects: delay/echo, tremolo, comb reverb."""

from pyminidsp._minidsp_cffi import lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array


def delay_echo(signal, delay_samples, feedback=0.5, dry=1.0, wet=0.5):
    """
    Apply a delay/echo effect.

    Args:
        signal: Input signal.
        delay_samples: Delay length in samples.
        feedback: Echo feedback gain (|feedback| < 1).
        dry: Dry mix weight.
        wet: Wet mix weight.

    Returns:
        numpy array of the processed signal.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_delay_echo(s_ptr, out_ptr, n, delay_samples, feedback, dry, wet)
    return out


def tremolo(signal, rate_hz, depth=0.5, sample_rate=44100.0):
    """
    Apply a tremolo effect (amplitude modulation).

    Args:
        signal: Input signal.
        rate_hz: LFO rate in Hz.
        depth: Modulation depth in [0, 1].
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of the processed signal.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_tremolo(s_ptr, out_ptr, n, rate_hz, depth, sample_rate)
    return out


def comb_reverb(signal, delay_samples, feedback=0.5, dry=1.0, wet=0.3):
    """
    Apply a comb-filter reverb effect.

    Args:
        signal: Input signal.
        delay_samples: Comb delay in samples.
        feedback: Feedback gain (|feedback| < 1).
        dry: Dry mix weight.
        wet: Wet mix weight.

    Returns:
        numpy array of the processed signal.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_comb_reverb(s_ptr, out_ptr, n, delay_samples, feedback, dry, wet)
    return out
