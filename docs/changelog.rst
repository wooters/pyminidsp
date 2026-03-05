Changelog
=========

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
