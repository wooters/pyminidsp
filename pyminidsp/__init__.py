"""
pyminidsp - Python bindings to the miniDSP C library.

A comprehensive DSP toolkit providing signal generation, spectral analysis,
filtering, effects, and more. All functions accept and return NumPy arrays.

Example:
    >>> import pyminidsp as md
    >>> signal = md.sine_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
    >>> mag = md.magnitude_spectrum(signal)
    >>> md.shutdown()
"""

from pyminidsp._core import *  # noqa: F401, F403
from pyminidsp._core import (
    # Re-export everything explicitly for documentation
    # Signal measurement
    dot, entropy, energy, power, power_db,
    # Signal analysis
    rms, zero_crossing_rate, autocorrelation, peak_detect,
    f0_autocorrelation, f0_fft, mix,
    # Effects
    delay_echo, tremolo, comb_reverb,
    # FIR / Convolution
    convolution_num_samples, convolution_time, moving_average,
    fir_filter, convolution_fft_ola,
    # Scaling
    scale, scale_vec, fit_within_range, adjust_dblevel,
    # Spectrum
    magnitude_spectrum, power_spectral_density, phase_spectrum,
    stft_num_frames, stft, mel_filterbank, mel_energies, mfcc,
    # Windows
    hann_window, hamming_window, blackman_window, rect_window,
    # Generators
    sine_wave, white_noise, impulse, chirp_linear, chirp_log,
    square_wave, sawtooth_wave, shepard_tone,
    # DTMF
    dtmf_detect, dtmf_generate, dtmf_signal_length,
    # Cleanup
    shutdown,
    # GCC
    get_delay, get_multiple_delays, gcc,
    # Spectrogram text
    spectrogram_text,
    # Steganography
    steg_capacity, steg_encode, steg_decode,
    steg_encode_bytes, steg_decode_bytes, steg_detect,
    # Biquad
    BiquadFilter,
    # Constants
    LPF, HPF, BPF, NOTCH, PEQ, LSH, HSH,
    STEG_LSB, STEG_FREQ_BAND, STEG_TYPE_TEXT, STEG_TYPE_BINARY,
    GCC_SIMP, GCC_PHAT,
)

__version__ = "0.1.0"
__all__ = [
    # Signal measurement
    "dot", "entropy", "energy", "power", "power_db",
    # Signal analysis
    "rms", "zero_crossing_rate", "autocorrelation", "peak_detect",
    "f0_autocorrelation", "f0_fft", "mix",
    # Effects
    "delay_echo", "tremolo", "comb_reverb",
    # FIR / Convolution
    "convolution_num_samples", "convolution_time", "moving_average",
    "fir_filter", "convolution_fft_ola",
    # Scaling
    "scale", "scale_vec", "fit_within_range", "adjust_dblevel",
    # Spectrum
    "magnitude_spectrum", "power_spectral_density", "phase_spectrum",
    "stft_num_frames", "stft", "mel_filterbank", "mel_energies", "mfcc",
    # Windows
    "hann_window", "hamming_window", "blackman_window", "rect_window",
    # Generators
    "sine_wave", "white_noise", "impulse", "chirp_linear", "chirp_log",
    "square_wave", "sawtooth_wave", "shepard_tone",
    # DTMF
    "dtmf_detect", "dtmf_generate", "dtmf_signal_length",
    # Cleanup
    "shutdown",
    # GCC
    "get_delay", "get_multiple_delays", "gcc",
    # Spectrogram text
    "spectrogram_text",
    # Steganography
    "steg_capacity", "steg_encode", "steg_decode",
    "steg_encode_bytes", "steg_decode_bytes", "steg_detect",
    # Biquad
    "BiquadFilter",
    # Constants
    "LPF", "HPF", "BPF", "NOTCH", "PEQ", "LSH", "HSH",
    "STEG_LSB", "STEG_FREQ_BAND", "STEG_TYPE_TEXT", "STEG_TYPE_BINARY",
    "GCC_SIMP", "GCC_PHAT",
]
