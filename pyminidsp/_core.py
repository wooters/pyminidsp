"""
Core Python bindings wrapping the miniDSP C library via CFFI.

All functions accept and return NumPy arrays (float64). Input arrays are
automatically converted to contiguous float64 before being passed to C.
"""

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
# Signal measurement
# ---------------------------------------------------------------------------

def dot(a, b):
    """Compute the dot product of two vectors."""
    a_ptr, a = _as_double_ptr(a)
    b_ptr, b = _as_double_ptr(b)
    n = min(len(a), len(b))
    return lib.MD_dot(a_ptr, b_ptr, n)


def entropy(a, clip=False):
    """Compute the normalized entropy of a distribution."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_entropy(a_ptr, len(a), clip)


def energy(a):
    """Compute signal energy: sum of squared samples."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_energy(a_ptr, len(a))


def power(a):
    """Compute signal power: energy / N."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_power(a_ptr, len(a))


def power_db(a):
    """Compute signal power in decibels."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_power_db(a_ptr, len(a))


# ---------------------------------------------------------------------------
# Signal analysis
# ---------------------------------------------------------------------------

def rms(a):
    """Compute the root mean square (RMS) of a signal."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_rms(a_ptr, len(a))


def zero_crossing_rate(a):
    """Compute the zero-crossing rate of a signal."""
    a_ptr, a = _as_double_ptr(a)
    return lib.MD_zero_crossing_rate(a_ptr, len(a))


def autocorrelation(a, max_lag):
    """
    Compute the normalised autocorrelation of a signal.

    Args:
        a: Input signal.
        max_lag: Number of lag values to compute.

    Returns:
        numpy array of autocorrelation values, length max_lag.
    """
    a_ptr, a = _as_double_ptr(a)
    out, out_ptr = _new_double_array(max_lag)
    lib.MD_autocorrelation(a_ptr, len(a), out_ptr, max_lag)
    return out


def peak_detect(a, threshold=0.0, min_distance=1):
    """
    Detect peaks (local maxima) in a signal.

    Args:
        a: Input signal.
        threshold: Minimum value for a peak.
        min_distance: Minimum index gap between peaks.

    Returns:
        numpy array of peak indices.
    """
    a_ptr, a = _as_double_ptr(a)
    n = len(a)
    peaks = np.zeros(n, dtype=np.uint32)
    num_peaks = ffi.new("unsigned *")
    lib.MD_peak_detect(
        a_ptr, n, threshold, min_distance,
        ffi.cast("unsigned *", peaks.ctypes.data), num_peaks,
    )
    return peaks[: num_peaks[0]].copy()


def f0_autocorrelation(signal, sample_rate, min_freq_hz=80.0, max_freq_hz=400.0):
    """Estimate F0 using autocorrelation."""
    s_ptr, signal = _as_double_ptr(signal)
    return lib.MD_f0_autocorrelation(s_ptr, len(signal), sample_rate, min_freq_hz, max_freq_hz)


def f0_fft(signal, sample_rate, min_freq_hz=80.0, max_freq_hz=400.0):
    """Estimate F0 using FFT peak picking."""
    s_ptr, signal = _as_double_ptr(signal)
    return lib.MD_f0_fft(s_ptr, len(signal), sample_rate, min_freq_hz, max_freq_hz)


def mix(a, b, w_a=0.5, w_b=0.5):
    """
    Mix (weighted sum) two signals.

    Args:
        a, b: Input signals of the same length.
        w_a, w_b: Weights for signals a and b.

    Returns:
        numpy array of the mixed signal.
    """
    a_ptr, a = _as_double_ptr(a)
    b_ptr, b = _as_double_ptr(b)
    n = min(len(a), len(b))
    out, out_ptr = _new_double_array(n)
    lib.MD_mix(a_ptr, b_ptr, out_ptr, n, w_a, w_b)
    return out


# ---------------------------------------------------------------------------
# Simple effects
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# FIR filters / convolution
# ---------------------------------------------------------------------------

def convolution_num_samples(signal_len, kernel_len):
    """Compute the output length of a full linear convolution."""
    return lib.MD_convolution_num_samples(signal_len, kernel_len)


def convolution_time(signal, kernel):
    """
    Time-domain full linear convolution.

    Returns:
        numpy array of length signal_len + kernel_len - 1.
    """
    s_ptr, signal = _as_double_ptr(signal)
    k_ptr, kernel = _as_double_ptr(kernel)
    out_len = len(signal) + len(kernel) - 1
    out, out_ptr = _new_double_array(out_len)
    lib.MD_convolution_time(s_ptr, len(signal), k_ptr, len(kernel), out_ptr)
    return out


def moving_average(signal, window_len):
    """
    Causal moving-average FIR filter.

    Returns:
        numpy array of the same length as the input.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_moving_average(s_ptr, n, window_len, out_ptr)
    return out


def fir_filter(signal, coeffs):
    """
    Apply a causal FIR filter with arbitrary coefficients.

    Returns:
        numpy array of the same length as the input.
    """
    s_ptr, signal = _as_double_ptr(signal)
    c_ptr, coeffs = _as_double_ptr(coeffs)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_fir_filter(s_ptr, n, c_ptr, len(coeffs), out_ptr)
    return out


def convolution_fft_ola(signal, kernel):
    """
    Full linear convolution using FFT overlap-add.

    Returns:
        numpy array of length signal_len + kernel_len - 1.
    """
    s_ptr, signal = _as_double_ptr(signal)
    k_ptr, kernel = _as_double_ptr(kernel)
    out_len = len(signal) + len(kernel) - 1
    out, out_ptr = _new_double_array(out_len)
    lib.MD_convolution_fft_ola(s_ptr, len(signal), k_ptr, len(kernel), out_ptr)
    return out


# ---------------------------------------------------------------------------
# Signal scaling
# ---------------------------------------------------------------------------

def scale(value, oldmin, oldmax, newmin, newmax):
    """Map a single value from one range to another."""
    return lib.MD_scale(value, oldmin, oldmax, newmin, newmax)


def scale_vec(a, oldmin, oldmax, newmin, newmax):
    """Map every element of a vector from one range to another."""
    a_ptr, a_arr = _as_double_ptr(a)
    n = len(a_arr)
    out, out_ptr = _new_double_array(n)
    # MD_scale_vec takes non-const input pointer
    in_copy = np.array(a_arr, dtype=np.float64, copy=True)
    in_ptr = ffi.cast("double *", in_copy.ctypes.data)
    lib.MD_scale_vec(in_ptr, out_ptr, n, oldmin, oldmax, newmin, newmax)
    return out


def fit_within_range(a, newmin, newmax):
    """Fit values within [newmin, newmax]."""
    a_arr = np.ascontiguousarray(a, dtype=np.float64)
    n = len(a_arr)
    in_copy = np.array(a_arr, copy=True)
    in_ptr = ffi.cast("double *", in_copy.ctypes.data)
    out, out_ptr = _new_double_array(n)
    lib.MD_fit_within_range(in_ptr, out_ptr, n, newmin, newmax)
    return out


def adjust_dblevel(signal, dblevel):
    """Automatic Gain Control: scale signal to target dB level, clip to [-1, 1]."""
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(n)
    lib.MD_adjust_dblevel(s_ptr, out_ptr, n, dblevel)
    return out


# ---------------------------------------------------------------------------
# FFT / Spectrum analysis
# ---------------------------------------------------------------------------

def magnitude_spectrum(signal):
    """
    Compute the magnitude spectrum of a real-valued signal.

    Returns:
        numpy array of length N/2 + 1 containing |X(k)|.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_magnitude_spectrum(s_ptr, n, out_ptr)
    return out


def power_spectral_density(signal):
    """
    Compute the power spectral density (PSD) of a signal.

    Returns:
        numpy array of length N/2 + 1 containing |X(k)|^2 / N.
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_power_spectral_density(s_ptr, n, out_ptr)
    return out


def phase_spectrum(signal):
    """
    Compute the one-sided phase spectrum in radians.

    Returns:
        numpy array of length N/2 + 1 with phase in [-pi, pi].
    """
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_bins)
    lib.MD_phase_spectrum(s_ptr, n, out_ptr)
    return out


def stft_num_frames(signal_len, n, hop):
    """Compute the number of STFT frames."""
    return lib.MD_stft_num_frames(signal_len, n, hop)


def stft(signal, n, hop):
    """
    Compute the Short-Time Fourier Transform (STFT).

    Args:
        signal: Input signal.
        n: FFT window size.
        hop: Hop size in samples.

    Returns:
        2D numpy array of shape (num_frames, n//2+1) containing magnitudes.
    """
    s_ptr, signal = _as_double_ptr(signal)
    signal_len = len(signal)
    num_frames = lib.MD_stft_num_frames(signal_len, n, hop)
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_frames * num_bins)
    lib.MD_stft(s_ptr, signal_len, n, hop, out_ptr)
    return out.reshape(num_frames, num_bins)


def mel_filterbank(n, sample_rate, num_mels=26, min_freq_hz=0.0, max_freq_hz=None):
    """
    Build a mel-spaced triangular filterbank matrix.

    Args:
        n: FFT size.
        sample_rate: Sampling rate in Hz.
        num_mels: Number of mel filters.
        min_freq_hz: Lower frequency bound.
        max_freq_hz: Upper frequency bound (defaults to sample_rate/2).

    Returns:
        2D numpy array of shape (num_mels, n//2+1).
    """
    if max_freq_hz is None:
        max_freq_hz = sample_rate / 2.0
    num_bins = n // 2 + 1
    out, out_ptr = _new_double_array(num_mels * num_bins)
    lib.MD_mel_filterbank(n, sample_rate, num_mels, min_freq_hz, max_freq_hz, out_ptr)
    return out.reshape(num_mels, num_bins)


def mel_energies(signal, sample_rate, num_mels=26, min_freq_hz=0.0, max_freq_hz=None):
    """
    Compute mel-band energies from a single frame.

    Returns:
        numpy array of length num_mels.
    """
    if max_freq_hz is None:
        max_freq_hz = sample_rate / 2.0
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(num_mels)
    lib.MD_mel_energies(s_ptr, n, sample_rate, num_mels, min_freq_hz, max_freq_hz, out_ptr)
    return out


def mfcc(signal, sample_rate, num_mels=26, num_coeffs=13,
         min_freq_hz=0.0, max_freq_hz=None):
    """
    Compute MFCCs from a single frame.

    Args:
        signal: Input frame.
        sample_rate: Sampling rate in Hz.
        num_mels: Number of mel bands.
        num_coeffs: Number of cepstral coefficients to output.
        min_freq_hz: Lower frequency bound.
        max_freq_hz: Upper frequency bound (defaults to sample_rate/2).

    Returns:
        numpy array of length num_coeffs.
    """
    if max_freq_hz is None:
        max_freq_hz = sample_rate / 2.0
    s_ptr, signal = _as_double_ptr(signal)
    n = len(signal)
    out, out_ptr = _new_double_array(num_coeffs)
    lib.MD_mfcc(s_ptr, n, sample_rate, num_mels, num_coeffs,
                min_freq_hz, max_freq_hz, out_ptr)
    return out


# ---------------------------------------------------------------------------
# Window generation
# ---------------------------------------------------------------------------

def hann_window(n):
    """Generate a Hanning (Hann) window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Hann_Win(out_ptr, n)
    return out


def hamming_window(n):
    """Generate a Hamming window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Hamming_Win(out_ptr, n)
    return out


def blackman_window(n):
    """Generate a Blackman window of length n."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Blackman_Win(out_ptr, n)
    return out


def rect_window(n):
    """Generate a rectangular window of length n (all ones)."""
    out, out_ptr = _new_double_array(n)
    lib.MD_Gen_Rect_Win(out_ptr, n)
    return out


# ---------------------------------------------------------------------------
# Signal generators
# ---------------------------------------------------------------------------

def sine_wave(n, amplitude=1.0, freq=440.0, sample_rate=44100.0):
    """
    Generate a sine wave.

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        freq: Frequency in Hz.
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_sine_wave(out_ptr, n, amplitude, freq, sample_rate)
    return out


def white_noise(n, amplitude=1.0, seed=42):
    """
    Generate Gaussian white noise.

    Args:
        n: Number of samples.
        amplitude: Standard deviation.
        seed: Random seed for reproducibility.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_white_noise(out_ptr, n, amplitude, seed)
    return out


def impulse(n, amplitude=1.0, position=0):
    """
    Generate a discrete impulse (Kronecker delta).

    Args:
        n: Number of samples.
        amplitude: Spike amplitude.
        position: Sample index of the spike.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_impulse(out_ptr, n, amplitude, position)
    return out


def chirp_linear(n, amplitude=1.0, f_start=200.0, f_end=4000.0, sample_rate=16000.0):
    """
    Generate a linear chirp (swept sine).

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        f_start: Starting frequency in Hz.
        f_end: Ending frequency in Hz.
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_chirp_linear(out_ptr, n, amplitude, f_start, f_end, sample_rate)
    return out


def chirp_log(n, amplitude=1.0, f_start=20.0, f_end=20000.0, sample_rate=44100.0):
    """
    Generate a logarithmic chirp.

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        f_start: Starting frequency in Hz (must be > 0).
        f_end: Ending frequency in Hz (must be > 0, != f_start).
        sample_rate: Sampling rate in Hz.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_chirp_log(out_ptr, n, amplitude, f_start, f_end, sample_rate)
    return out


def square_wave(n, amplitude=1.0, freq=440.0, sample_rate=44100.0):
    """Generate a square wave."""
    out, out_ptr = _new_double_array(n)
    lib.MD_square_wave(out_ptr, n, amplitude, freq, sample_rate)
    return out


def sawtooth_wave(n, amplitude=1.0, freq=440.0, sample_rate=44100.0):
    """Generate a sawtooth wave."""
    out, out_ptr = _new_double_array(n)
    lib.MD_sawtooth_wave(out_ptr, n, amplitude, freq, sample_rate)
    return out


def shepard_tone(n, amplitude=0.8, base_freq=440.0, sample_rate=44100.0,
                 rate_octaves_per_sec=0.5, num_octaves=8):
    """
    Generate a Shepard tone (auditory illusion of endlessly rising/falling pitch).

    Args:
        n: Number of samples.
        amplitude: Peak amplitude.
        base_freq: Centre frequency of the Gaussian envelope in Hz.
        sample_rate: Sampling rate in Hz.
        rate_octaves_per_sec: Glissando rate (positive=rising, negative=falling).
        num_octaves: Number of audible octave layers.

    Returns:
        numpy array of length n.
    """
    out, out_ptr = _new_double_array(n)
    lib.MD_shepard_tone(out_ptr, n, amplitude, base_freq, sample_rate,
                        rate_octaves_per_sec, num_octaves)
    return out


# ---------------------------------------------------------------------------
# DTMF
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------

def shutdown():
    """Free all internally cached FFT plans and buffers."""
    lib.MD_shutdown()


# Register shutdown to run at interpreter exit
atexit.register(shutdown)


# ---------------------------------------------------------------------------
# GCC delay estimation
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Spectrogram text
# ---------------------------------------------------------------------------

def spectrogram_text(text, freq_lo=200.0, freq_hi=7500.0,
                     duration_sec=2.0, sample_rate=16000.0):
    """
    Synthesise audio that displays readable text in a spectrogram.

    Args:
        text: ASCII string to render.
        freq_lo: Lowest frequency in Hz.
        freq_hi: Highest frequency in Hz.
        duration_sec: Total duration in seconds.
        sample_rate: Sample rate in Hz.

    Returns:
        numpy array of audio samples.
    """
    max_len = int(duration_sec * sample_rate) + 1024
    out, out_ptr = _new_double_array(max_len)
    text_bytes = text.encode("ascii")
    n_written = lib.MD_spectrogram_text(out_ptr, max_len, text_bytes,
                                         freq_lo, freq_hi,
                                         duration_sec, sample_rate)
    return out[:n_written].copy()


# ---------------------------------------------------------------------------
# Steganography
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Biquad filter
# ---------------------------------------------------------------------------

class BiquadFilter:
    """
    Biquad (second-order IIR) filter.

    Supports low-pass, high-pass, band-pass, notch, peaking EQ,
    low shelf, and high shelf filter types.

    Example:
        >>> filt = BiquadFilter(LPF, freq=1000.0, sample_rate=44100.0)
        >>> for sample in signal:
        ...     output = filt.process(sample)
    """

    def __init__(self, filter_type, freq, sample_rate, db_gain=0.0, bandwidth=1.0):
        """
        Create a new biquad filter.

        Args:
            filter_type: One of LPF, HPF, BPF, NOTCH, PEQ, LSH, HSH.
            freq: Centre/corner frequency in Hz.
            sample_rate: Sampling rate in Hz.
            db_gain: Gain in dB (only for PEQ, LSH, HSH).
            bandwidth: Bandwidth in octaves.
        """
        self._ptr = lib.BiQuad_new(filter_type, db_gain, freq, sample_rate, bandwidth)
        if self._ptr == ffi.NULL:
            raise MemoryError("Failed to allocate biquad filter")

    def __del__(self):
        if hasattr(self, "_ptr") and self._ptr != ffi.NULL:
            lib.free(self._ptr)
            self._ptr = ffi.NULL

    def process(self, sample):
        """Process a single sample through the filter."""
        return lib.BiQuad(sample, self._ptr)

    def process_array(self, signal):
        """
        Process an entire signal through the filter.

        Args:
            signal: Input numpy array.

        Returns:
            Filtered numpy array.
        """
        signal = np.asarray(signal, dtype=np.float64)
        out = np.empty_like(signal)
        for i in range(len(signal)):
            out[i] = lib.BiQuad(signal[i], self._ptr)
        return out
