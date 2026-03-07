# pyminidsp

**[Documentation](https://wooters.github.io/pyminidsp/)**

Python bindings to the [miniDSP](https://github.com/wooters/miniDSP) C library.

A comprehensive DSP toolkit providing signal generation, spectral analysis,
filtering, effects, and more. All functions accept and return NumPy arrays.

## Prerequisites

- Python >= 3.9
- [FFTW3](http://www.fftw.org/) development headers
  - Ubuntu/Debian: `sudo apt install libfftw3-dev`
  - macOS: `brew install fftw`
- A C compiler (gcc or clang)

## Installation

```bash
# Clone the miniDSP C library (if not already present)
git clone https://github.com/wooters/miniDSP.git

# Create virtual environment (uses .python-version for Python version)
uv venv

# Install pyminidsp (set MINIDSP_SRC to point to the C library)
MINIDSP_SRC=./miniDSP uv sync
```

Or for development:

```bash
MINIDSP_SRC=./miniDSP uv sync --extra dev
```

## Quick Start

```python
import pyminidsp as md

# Generate a 440 Hz sine wave (1 second at 44.1 kHz)
signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)

# Compute the magnitude spectrum
mag = md.magnitude_spectrum(signal)

# Compute MFCCs from a frame
coeffs = md.mfcc(signal[:512], sample_rate=44100.0, num_mels=26, num_coeffs=13)

# Apply a low-pass biquad filter
lpf = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
filtered = lpf.process_array(signal)

# Clean up FFT caches when done
md.shutdown()
```

## API Overview

### Signal Generators

| Function | Description |
|----------|-------------|
| `sine_wave(n, amplitude, freq, sample_rate)` | Pure sine tone |
| `white_noise(n, amplitude, seed)` | Gaussian white noise |
| `impulse(n, amplitude, position)` | Kronecker delta |
| `chirp_linear(n, amplitude, f_start, f_end, sample_rate)` | Linear frequency sweep |
| `chirp_log(n, amplitude, f_start, f_end, sample_rate)` | Logarithmic frequency sweep |
| `square_wave(n, amplitude, freq, sample_rate)` | Square wave |
| `sawtooth_wave(n, amplitude, freq, sample_rate)` | Sawtooth wave |
| `shepard_tone(n, amplitude, base_freq, sample_rate, rate, num_octaves)` | Shepard tone illusion |

### Spectral Analysis

| Function | Description |
|----------|-------------|
| `magnitude_spectrum(signal)` | One-sided magnitude spectrum via FFT |
| `power_spectral_density(signal)` | Periodogram PSD estimate |
| `phase_spectrum(signal)` | Phase spectrum in radians |
| `stft(signal, n, hop)` | Short-Time Fourier Transform |
| `mel_filterbank(n, sample_rate, num_mels)` | Mel-spaced triangular filterbank |
| `mel_energies(signal, sample_rate, num_mels)` | Mel-band energies |
| `mfcc(signal, sample_rate, num_mels, num_coeffs)` | Mel-frequency cepstral coefficients |

### Signal Analysis

| Function | Description |
|----------|-------------|
| `rms(signal)` | Root mean square |
| `energy(signal)` | Signal energy |
| `power(signal)` / `power_db(signal)` | Signal power (linear / dB) |
| `zero_crossing_rate(signal)` | Zero-crossing rate |
| `autocorrelation(signal, max_lag)` | Normalised autocorrelation |
| `peak_detect(signal, threshold, min_distance)` | Local maxima detection |
| `f0_autocorrelation(signal, sample_rate, min_freq, max_freq)` | F0 via autocorrelation |
| `f0_fft(signal, sample_rate, min_freq, max_freq)` | F0 via FFT peak picking |

### Effects & Filters

| Function | Description |
|----------|-------------|
| `delay_echo(signal, delay_samples, feedback, dry, wet)` | Echo effect |
| `tremolo(signal, rate_hz, depth, sample_rate)` | Amplitude modulation |
| `comb_reverb(signal, delay_samples, feedback, dry, wet)` | Comb-filter reverb |
| `convolution_time(signal, kernel)` | Time-domain convolution |
| `convolution_fft_ola(signal, kernel)` | FFT overlap-add convolution |
| `moving_average(signal, window_len)` | Moving average filter |
| `fir_filter(signal, coeffs)` | FIR filter |
| `BiquadFilter(type, freq, sample_rate)` | IIR biquad filter (LPF/HPF/BPF/etc.) |

### DTMF

| Function | Description |
|----------|-------------|
| `dtmf_generate(digits, sample_rate, tone_ms, pause_ms)` | Generate DTMF tones |
| `dtmf_detect(signal, sample_rate)` | Detect DTMF digits |

### Delay Estimation (GCC-PHAT)

| Function | Description |
|----------|-------------|
| `get_delay(sig_a, sig_b, margin, weighting)` | Delay between two signals |
| `gcc(sig_a, sig_b, weighting)` | Full cross-correlation |

### Audio Steganography

| Function | Description |
|----------|-------------|
| `steg_encode(host, message, sample_rate, method)` | Hide text in audio |
| `steg_decode(stego, sample_rate, method)` | Recover hidden text |
| `steg_encode_bytes(host, data, sample_rate, method)` | Hide binary data |
| `steg_decode_bytes(stego, sample_rate, method)` | Recover binary data |
| `steg_detect(signal, sample_rate)` | Detect steganography method |

### Spectrogram Art

| Function | Description |
|----------|-------------|
| `spectrogram_text(text, freq_lo, freq_hi, duration, sample_rate)` | Text visible in spectrogram |

## Running Tests

```bash
MINIDSP_SRC=./miniDSP uv run pytest tests/ -v
```

## License

MIT
