"""Shared constants, CFFI helpers, and cleanup for pyminidsp submodules."""

from __future__ import annotations

import atexit
from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt

from pyminidsp._minidsp_cffi import ffi, lib

if TYPE_CHECKING:
    from pyminidsp._minidsp_cffi import CData

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Biquad filter types
LPF: int = 0    # Low-pass filter
HPF: int = 1    # High-pass filter
BPF: int = 2    # Band-pass filter
NOTCH: int = 3  # Notch filter
PEQ: int = 4    # Peaking EQ
LSH: int = 5    # Low shelf
HSH: int = 6    # High shelf

# Steganography methods
STEG_LSB: int = 0
STEG_FREQ_BAND: int = 1
STEG_SPECTEXT: int = 2
STEG_TYPE_TEXT: int = 0
STEG_TYPE_BINARY: int = 1

# GCC weighting types
GCC_SIMP: int = 0
GCC_PHAT: int = 1

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _as_double_ptr(arr: npt.ArrayLike) -> tuple[CData, npt.NDArray[np.float64]]:
    """Convert a numpy array to a contiguous float64 array and return a CFFI pointer."""
    a = np.ascontiguousarray(arr, dtype=np.float64)
    return ffi.cast("const double *", a.ctypes.data), a


def _new_double_array(n: int) -> tuple[npt.NDArray[np.float64], CData]:
    """Allocate a numpy float64 array and return (array, cffi_ptr)."""
    a = np.zeros(n, dtype=np.float64)
    return a, ffi.cast("double *", a.ctypes.data)


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def shutdown() -> None:
    """Free all internally cached FFT plans and buffers."""
    lib.MD_shutdown()


# Register shutdown to run at interpreter exit
atexit.register(shutdown)
