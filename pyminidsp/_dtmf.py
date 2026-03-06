"""DTMF tone generation and detection."""

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array


def dtmf_signal_length(num_digits, sample_rate=8000.0, tone_ms=70, pause_ms=70):
    """Calculate the number of samples needed for dtmf_generate()."""
    return lib.MD_dtmf_signal_length(num_digits, sample_rate, tone_ms, pause_ms)


def dtmf_generate(digits, sample_rate=8000.0, tone_ms=70, pause_ms=70):
    """
    Generate a DTMF tone sequence.

    Args:
        digits: String of DTMF characters ('0'-'9', 'A'-'D', '*', '#').
        sample_rate: Sampling rate in Hz.
        tone_ms: Duration of each tone in ms (>= 40).
        pause_ms: Duration of silence between tones in ms (>= 40).

    Returns:
        numpy array of audio samples.
    """
    num_digits = len(digits)
    sig_len = lib.MD_dtmf_signal_length(num_digits, sample_rate, tone_ms, pause_ms)
    out, out_ptr = _new_double_array(sig_len)
    digits_bytes = digits.encode("ascii")
    lib.MD_dtmf_generate(out_ptr, digits_bytes, sample_rate, tone_ms, pause_ms)
    return out


def dtmf_detect(signal, sample_rate=8000.0, max_tones=64):
    """
    Detect DTMF tones in an audio signal.

    Args:
        signal: Audio samples.
        sample_rate: Sampling rate in Hz.
        max_tones: Maximum number of tones to detect.

    Returns:
        List of (digit, start_s, end_s) tuples.
    """
    s_ptr, signal = _as_double_ptr(signal)
    tones = ffi.new("MD_DTMFTone[]", max_tones)
    n = lib.MD_dtmf_detect(s_ptr, len(signal), sample_rate, tones, max_tones)
    result = []
    for i in range(n):
        digit = tones[i].digit
        # CFFI returns char as bytes
        if isinstance(digit, bytes):
            digit = digit.decode("ascii")
        else:
            digit = chr(digit)
        result.append((digit, tones[i].start_s, tones[i].end_s))
    return result
