"""Shared constants, CFFI helpers, and cleanup for pyminidsp submodules."""

import atexit

import numpy as np

from pyminidsp._minidsp_cffi import ffi, lib

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Biquad filter types
LPF = 0    # Low-pass filter
HPF = 1    # High-pass filter
BPF = 2    # Band-pass filter
NOTCH = 3  # Notch filter
PEQ = 4    # Peaking EQ
LSH = 5    # Low shelf
HSH = 6    # High shelf

# Steganography methods
STEG_LSB = 0
STEG_FREQ_BAND = 1
STEG_TYPE_TEXT = 0
STEG_TYPE_BINARY = 1

# GCC weighting types
GCC_SIMP = 0
GCC_PHAT = 1

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _as_double_ptr(arr):
    """Convert a numpy array to a contiguous float64 array and return a CFFI pointer."""
    arr = np.ascontiguousarray(arr, dtype=np.float64)
    return ffi.cast("const double *", arr.ctypes.data), arr


def _new_double_array(n):
    """Allocate a numpy float64 array and return (array, cffi_ptr)."""
    arr = np.zeros(n, dtype=np.float64)
    return arr, ffi.cast("double *", arr.ctypes.data)


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def shutdown():
    """Free all internally cached FFT plans and buffers."""
    lib.MD_shutdown()


# Register shutdown to run at interpreter exit
atexit.register(shutdown)
