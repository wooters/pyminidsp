Quick Start
===========

Basic usage
-----------

Every function in pyminidsp accepts and returns NumPy ``float64`` arrays.
Input arrays are automatically converted if needed.

.. code-block:: python

   import pyminidsp as md

   # Generate a 440 Hz sine wave (1 second at 44.1 kHz)
   signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)

   # Check the signal's RMS level (unit sine ≈ 0.707)
   print(md.rms(signal))

   # Always call shutdown() when done to free internal FFT caches
   md.shutdown()

.. note::

   :func:`~pyminidsp.shutdown` is registered with :mod:`atexit`, so it
   runs automatically at interpreter exit.  You can also call it explicitly
   to free memory sooner.


Signal generation
-----------------

pyminidsp provides a range of test signal generators:

.. code-block:: python

   # Gaussian white noise (reproducible via seed)
   noise = md.white_noise(4096, amplitude=1.0, seed=42)

   # Linear chirp from 200 Hz to 4 kHz
   chirp = md.chirp_linear(16000, f_start=200.0, f_end=4000.0, sample_rate=16000.0)

   # Shepard tone (endlessly rising pitch illusion)
   shepard = md.shepard_tone(44100, amplitude=0.8, base_freq=440.0,
                              sample_rate=44100.0, rate_octaves_per_sec=0.5)


Spectral analysis
-----------------

.. code-block:: python

   # Magnitude spectrum (N/2 + 1 bins, from DC to Nyquist)
   mag = md.magnitude_spectrum(signal)

   # Short-Time Fourier Transform
   spec = md.stft(signal, n=512, hop=128)
   # spec.shape == (num_frames, 257)

   # Mel-frequency cepstral coefficients (single frame)
   coeffs = md.mfcc(signal[:512], sample_rate=44100.0, num_mels=26, num_coeffs=13)


Filtering
---------

.. code-block:: python

   # Biquad IIR filter (low-pass at 1 kHz)
   lpf = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
   filtered = lpf.process_array(signal)

   # FIR filter with custom coefficients
   import numpy as np
   coeffs = np.array([0.25, 0.5, 0.25])
   out = md.fir_filter(signal, coeffs)

   # FFT overlap-add convolution (faster for long kernels)
   out = md.convolution_fft_ola(signal, kernel)


DTMF encoding and decoding
---------------------------

.. code-block:: python

   # Generate a DTMF tone sequence
   sig = md.dtmf_generate("5551234", sample_rate=8000.0)

   # Detect tones in the signal
   tones = md.dtmf_detect(sig, sample_rate=8000.0)
   for digit, start_s, end_s in tones:
       print(f"{digit}  {start_s:.3f}–{end_s:.3f} s")


Delay estimation (GCC-PHAT)
----------------------------

.. code-block:: python

   import numpy as np

   # Simulate a delayed copy
   sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
   sig_b = np.roll(sig_a, 5)   # 5-sample delay

   delay, entropy = md.get_delay(sig_a, sig_b, margin=20, weighting=md.GCC_PHAT)
   print(f"Estimated delay: {delay} samples")


Audio steganography
-------------------

.. code-block:: python

   # Hide a secret message in audio
   host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
   stego, n_encoded = md.steg_encode(host, "secret message",
                                      sample_rate=44100.0, method=md.STEG_LSB)

   # Recover the message
   recovered = md.steg_decode(stego, sample_rate=44100.0, method=md.STEG_LSB)
   print(recovered)  # "secret message"
