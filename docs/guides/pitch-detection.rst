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

.. raw:: html

   <div style="display:flex;gap:0.75rem;margin:1em 0;flex-wrap:wrap;">
     <iframe src="../_static/plots/pitch_f0_tracks.html" style="flex:1;min-width:280px;height:380px;border:1px solid #ddd;border-radius:4px;" frameborder="0"></iframe>
     <iframe src="../_static/plots/pitch_acf_peak_frame.html" style="flex:1;min-width:280px;height:380px;border:1px solid #ddd;border-radius:4px;" frameborder="0"></iframe>
   </div>


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

.. raw:: html

   <iframe src="../_static/plots/pitch_fft_peak_frame.html" style="width:100%;max-width:600px;height:380px;border:1px solid #ddd;border-radius:4px;margin:1em 0;" frameborder="0"></iframe>


Practical notes
---------------

- **Search range** is critical for both methods.  Use prior knowledge of
  the expected pitch range (e.g. 80–400 Hz for speech).
- A return value of **0.0** means no reliable F0 was found — typically
  silence, unvoiced speech, or noisy frames.
- Longer frames improve resolution but reduce time accuracy.

.. code-block:: python

   md.shutdown()
