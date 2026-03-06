"""
Core Python bindings wrapping the miniDSP C library via CFFI.

All functions accept and return NumPy arrays (float64). Input arrays are
automatically converted to contiguous float64 before being passed to C.

This module re-exports the public API from the domain-specific submodules
so that existing ``from pyminidsp._core import X`` imports continue to work.
"""

# Constants and helpers
from pyminidsp._helpers import (  # noqa: F401
    LPF, HPF, BPF, NOTCH, PEQ, LSH, HSH,
    STEG_LSB, STEG_FREQ_BAND, STEG_TYPE_TEXT, STEG_TYPE_BINARY,
    GCC_SIMP, GCC_PHAT,
    _as_double_ptr, _new_double_array,
    shutdown,
)

# Signal measurement & analysis & scaling
from pyminidsp._analysis import (  # noqa: F401
    dot, entropy, energy, power, power_db,
    rms, zero_crossing_rate, autocorrelation, peak_detect,
    f0_autocorrelation, f0_fft, mix,
    scale, scale_vec, fit_within_range, adjust_dblevel,
)

# Effects
from pyminidsp._effects import delay_echo, tremolo, comb_reverb  # noqa: F401

# FIR filters / convolution / biquad
from pyminidsp._filters import (  # noqa: F401
    convolution_num_samples, convolution_time, moving_average,
    fir_filter, convolution_fft_ola,
    BiquadFilter,
)

# FFT / spectrum / mel / MFCC / windows
from pyminidsp._spectral import (  # noqa: F401
    magnitude_spectrum, power_spectral_density, phase_spectrum,
    stft_num_frames, stft, mel_filterbank, mel_energies, mfcc,
    hann_window, hamming_window, blackman_window, rect_window,
)

# Signal generators
from pyminidsp._generators import (  # noqa: F401
    sine_wave, white_noise, impulse, chirp_linear, chirp_log,
    square_wave, sawtooth_wave, shepard_tone,
    spectrogram_text,
)

# DTMF
from pyminidsp._dtmf import dtmf_signal_length, dtmf_generate, dtmf_detect  # noqa: F401

# GCC delay estimation
from pyminidsp._gcc import get_delay, get_multiple_delays, gcc  # noqa: F401

# Steganography
from pyminidsp._steganography import (  # noqa: F401
    steg_capacity, steg_encode, steg_decode,
    steg_encode_bytes, steg_decode_bytes, steg_detect,
)
