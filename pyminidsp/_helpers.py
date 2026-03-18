"""Shared constants, CFFI helpers, and cleanup for pyminidsp submodules."""

from __future__ import annotations

import atexit
import threading
from typing import TYPE_CHECKING

import numpy as np
import numpy.typing as npt

from pyminidsp._minidsp_cffi import ffi, lib

if TYPE_CHECKING:
    from pyminidsp._minidsp_cffi import CData

# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class MiniDSPError(RuntimeError):
    """Raised when the miniDSP C library reports an error."""

    def __init__(self, code: int, func_name: str, message: str) -> None:
        self.code = code
        self.func_name = func_name
        self.message = message
        super().__init__(f"{func_name}: {message} (code {code})")


# Error code constants matching MD_ErrorCode enum
ERR_NULL_POINTER: int = 1
ERR_INVALID_SIZE: int = 2
ERR_INVALID_RANGE: int = 3
ERR_ALLOC_FAILED: int = 4

# Thread-local storage for error state
_error_state = threading.local()


@ffi.def_extern()
def _pyminidsp_error_handler(code: int, func_name: CData, message: CData) -> None:
    """CFFI callback invoked by the C library on error."""
    _error_state.error = (
        int(code),
        ffi.string(func_name).decode("utf-8"),
        ffi.string(message).decode("utf-8"),
    )


def _check_error() -> None:
    """Check thread-local error state and raise MiniDSPError if set."""
    err = getattr(_error_state, "error", None)
    if err is not None:
        _error_state.error = None
        raise MiniDSPError(err[0], err[1], err[2])


# Register our Python callback as the C error handler
lib.MD_set_error_handler(lib._pyminidsp_error_handler)

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
