Changelog
=========

0.5.0 (2026-03-18)
-------------------

- Upgraded miniDSP C library from v0.3.1 to v0.4.0.
- New: ``MiniDSPError`` exception — C-level errors now raise Python exceptions
  instead of silently returning default values.
- New: ``ERR_NULL_POINTER``, ``ERR_INVALID_SIZE``, ``ERR_INVALID_RANGE``,
  ``ERR_ALLOC_FAILED`` error code constants.

0.4.0
-----

- Upgraded miniDSP C library from v0.1.0 to v0.3.1.
- New: ``design_lowpass_fir()`` — Kaiser-windowed sinc lowpass FIR filter design.
- New: ``lowpass_brickwall()`` — FFT-based ideal lowpass filter.
- New: ``kaiser_window()`` — Kaiser window with configurable beta parameter.
- New: ``resample()`` and ``resample_output_len()`` — polyphase sinc resampler.
- New: ``bessel_i0()`` and ``sinc()`` math utility functions.
- New: ``STEG_SPECTEXT`` constant for hybrid LSB + spectrogram text steganography.
- Includes upstream bug fixes (division-by-zero in minidsp_core.c).

0.3.0
-----

- Published on PyPI with Linux x86-64 and macOS ARM64 wheels.

0.1.0 (unreleased)
-------------------

- Initial release.
- Python bindings for the full miniDSP C library API via CFFI.
- Signal generators: sine, noise, impulse, chirp, square, sawtooth,
  Shepard tone.
- Spectral analysis: magnitude spectrum, PSD, phase spectrum, STFT,
  mel filterbank, mel energies, MFCCs.
- Signal analysis: RMS, zero-crossing rate, autocorrelation, peak
  detection, F0 estimation.
- Effects: delay/echo, tremolo, comb reverb.
- FIR filtering: time-domain convolution, moving average, FIR filter,
  FFT overlap-add convolution.
- Biquad IIR filters (LPF, HPF, BPF, notch, PEQ, low/high shelf).
- DTMF tone generation and detection.
- GCC-PHAT delay estimation.
- Audio steganography (LSB and frequency-band methods).
- Spectrogram text art synthesis.
