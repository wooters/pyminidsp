Pitch Detection
===============

Two methods for estimating the fundamental frequency (F0) of a signal.


Autocorrelation method
----------------------

Searches for the strongest peak in the normalised autocorrelation:

.. math::

   f_0 = \frac{f_s}{\tau_\text{peak}}

More robust for noisy or strongly harmonic signals.

.. code-block:: python

   import pyminidsp as md

   signal = md.sine_wave(4096, freq=200.0, sample_rate=16000.0)
   f0 = md.f0_autocorrelation(signal, sample_rate=16000.0,
                                min_freq_hz=80.0, max_freq_hz=400.0)
   print(f"Estimated F0: {f0:.1f} Hz")  # ≈ 200.0


FFT peak-picking method
-----------------------

Applies a Hann window, computes the magnitude spectrum, and identifies
the dominant peak in the requested frequency range:

.. math::

   f_0 = \frac{k_\text{peak} \cdot f_s}{N}

Simple and fast, but can lock onto harmonics (2f0, 3f0) when the
fundamental is weak.

.. code-block:: python

   f0 = md.f0_fft(signal, sample_rate=16000.0,
                   min_freq_hz=80.0, max_freq_hz=400.0)
   print(f"Estimated F0: {f0:.1f} Hz")  # ≈ 200.0


Practical notes
---------------

- **Search range** is critical for both methods.  Use prior knowledge of
  the expected pitch range (e.g. 80–400 Hz for speech).
- A return value of **0.0** means no reliable F0 was found — typically
  silence, unvoiced speech, or noisy frames.
- Longer frames improve resolution but reduce time accuracy.

.. code-block:: python

   md.shutdown()
