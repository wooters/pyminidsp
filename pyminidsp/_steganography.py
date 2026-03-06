"""Audio steganography: hide and recover data within audio signals."""

import numpy as np

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array, STEG_LSB


def steg_capacity(signal_len, sample_rate, method=STEG_LSB):
    """Compute maximum message length that can be hidden."""
    return lib.MD_steg_capacity(signal_len, sample_rate, method)


def steg_encode(host, message, sample_rate=44100.0, method=STEG_LSB):
    """
    Encode a secret text message into a host audio signal.

    Args:
        host: Host signal (not modified).
        message: String message to hide.
        sample_rate: Sample rate in Hz.
        method: STEG_LSB or STEG_FREQ_BAND.

    Returns:
        (stego_signal, num_bytes_encoded) tuple.
    """
    h_ptr, host = _as_double_ptr(host)
    n = len(host)
    out, out_ptr = _new_double_array(n)
    msg_bytes = message.encode("utf-8")
    encoded = lib.MD_steg_encode(h_ptr, out_ptr, n, sample_rate, msg_bytes, method)
    return out, encoded


def steg_decode(stego, sample_rate=44100.0, method=STEG_LSB, max_msg_len=4096):
    """
    Decode a secret text message from a stego audio signal.

    Returns:
        Decoded string message.
    """
    s_ptr, stego = _as_double_ptr(stego)
    msg_buf = ffi.new("char[]", max_msg_len)
    n = lib.MD_steg_decode(s_ptr, len(stego), sample_rate,
                           msg_buf, max_msg_len, method)
    if n == 0:
        return ""
    return ffi.string(msg_buf, n).decode("utf-8", errors="replace")


def steg_encode_bytes(host, data, sample_rate=44100.0, method=STEG_LSB):
    """
    Encode arbitrary binary data into a host audio signal.

    Args:
        host: Host signal.
        data: bytes-like object to hide.
        sample_rate: Sample rate in Hz.
        method: STEG_LSB or STEG_FREQ_BAND.

    Returns:
        (stego_signal, num_bytes_encoded) tuple.
    """
    h_ptr, host = _as_double_ptr(host)
    n = len(host)
    out, out_ptr = _new_double_array(n)
    data = bytes(data)
    data_ptr = ffi.from_buffer("const unsigned char *", data)
    encoded = lib.MD_steg_encode_bytes(h_ptr, out_ptr, n, sample_rate,
                                        data_ptr, len(data), method)
    return out, encoded


def steg_decode_bytes(stego, sample_rate=44100.0, method=STEG_LSB, max_len=4096):
    """
    Decode binary data from a stego audio signal.

    Returns:
        bytes object containing the decoded data.
    """
    s_ptr, stego = _as_double_ptr(stego)
    buf = np.zeros(max_len, dtype=np.uint8)
    buf_ptr = ffi.cast("unsigned char *", buf.ctypes.data)
    n = lib.MD_steg_decode_bytes(s_ptr, len(stego), sample_rate,
                                  buf_ptr, max_len, method)
    return bytes(buf[:n])


def steg_detect(signal, sample_rate=44100.0):
    """
    Detect which steganography method was used.

    Returns:
        (method, payload_type) tuple, or (None, None) if no steg detected.
        method is STEG_LSB, STEG_FREQ_BAND, or None.
        payload_type is STEG_TYPE_TEXT, STEG_TYPE_BINARY, or None.
    """
    s_ptr, signal = _as_double_ptr(signal)
    ptype = ffi.new("int *")
    method = lib.MD_steg_detect(s_ptr, len(signal), sample_rate, ptype)
    if method < 0:
        return None, None
    return method, ptype[0]
