Signal Analysis
===============

Time-domain analysis tools for characterising signal properties,
detecting features, and estimating pitch.

.. autofunction:: pyminidsp.rms

   Compute the root mean square (RMS) of a signal — the standard measure
   of signal "loudness":

   .. math::

      \mathrm{RMS} = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} x[n]^2}

   Equivalently, ``sqrt(power(a))``.  A unit-amplitude sine wave has
   RMS ≈ 0.707.  A DC signal of value *c* has RMS = |c|.

   .. code-block:: python

      signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)
      rms = md.rms(signal)  # ≈ 0.707

.. autofunction:: pyminidsp.zero_crossing_rate

   Count how often the signal changes sign, normalised by the number of
   adjacent pairs:

   .. math::

      \mathrm{ZCR} = \frac{1}{N-1}\sum_{n=1}^{N-1}
          \mathbf{1}\bigl[\mathrm{sgn}(x[n]) \ne \mathrm{sgn}(x[n-1])\bigr]

   Returns a value in [0.0, 1.0].  High ZCR indicates noise or
   high-frequency content; low ZCR indicates tonal or low-frequency
   content.

   .. code-block:: python

      signal = md.sine_wave(16000, freq=1000.0, sample_rate=16000.0)
      zcr = md.zero_crossing_rate(signal)
      # zcr ≈ 2 * 1000 / 16000 = 0.125

.. autofunction:: pyminidsp.autocorrelation

   Compute the normalised autocorrelation — measures the similarity
   between a signal and a delayed copy of itself:

   .. math::

      R[\tau] = \frac{1}{R[0]} \sum_{n=0}^{N-1-\tau} x[n]\,x[n+\tau]

   The output satisfies ``out[0] = 1.0`` and ``|out[tau]| <= 1.0``.
   A silent signal (all zeros) produces all-zero output.

   :param a: Input signal.
   :param max_lag: Number of lag values to compute.  Must be > 0 and < N.
   :returns: Array of autocorrelation values, length *max_lag*.

   .. code-block:: python

      signal = md.sine_wave(1024, freq=100.0, sample_rate=1000.0)
      acf = md.autocorrelation(signal, 50)
      # acf[0] = 1.0, acf[10] ≈ 1.0 (lag = one period of 100 Hz at 1 kHz)

.. autofunction:: pyminidsp.peak_detect

   Detect peaks (local maxima) in a signal.  A sample ``a[i]`` is a peak
   if it is strictly greater than both immediate neighbours and above the
   given threshold.  The *min_distance* parameter suppresses nearby
   secondary peaks.

   Peaks are found left-to-right.  Endpoint samples are never peaks
   because they lack two neighbours.

   :param a: Input signal.
   :param threshold: Minimum value for a peak.
   :param min_distance: Minimum index gap between accepted peaks (>= 1).
   :returns: Array of peak indices.

   .. code-block:: python

      import numpy as np
      signal = np.array([0, 1, 3, 1, 0, 2, 5, 2, 0], dtype=float)
      peaks = md.peak_detect(signal, threshold=0.0, min_distance=1)
      # peaks == [2, 6]  (values 3 and 5)

.. autofunction:: pyminidsp.f0_autocorrelation

   Estimate the fundamental frequency (F0) using autocorrelation.
   Searches for the strongest local peak in the normalised autocorrelation
   over lags corresponding to the requested frequency range:

   .. math::

      f_0 = \frac{f_s}{\tau_\text{peak}}

   :param signal: Input signal.
   :param sample_rate: Sampling rate in Hz (must be > 0).
   :param min_freq_hz: Minimum search frequency (must be > 0).
   :param max_freq_hz: Maximum search frequency (must be > *min_freq_hz*).
   :returns: Estimated F0 in Hz, or 0.0 if no reliable pitch is found.

.. autofunction:: pyminidsp.f0_fft

   Estimate F0 using FFT peak picking.  The signal is internally
   Hann-windowed, transformed, then the dominant magnitude peak in the
   requested frequency range is mapped back to Hz:

   .. math::

      f_0 = \frac{k_\text{peak} \cdot f_s}{N}

   Simple and fast, but generally less robust than
   :func:`f0_autocorrelation` for noisy or strongly harmonic signals.

.. autofunction:: pyminidsp.mix

   Mix (weighted sum) two signals element-wise:

   .. math::

      \mathrm{out}[n] = w_a \cdot a[n] + w_b \cdot b[n]

   :param a: First input signal.
   :param b: Second input signal (same length as *a*).
   :param w_a: Weight for signal *a*.
   :param w_b: Weight for signal *b*.
   :returns: Mixed signal array.

   .. code-block:: python

      sine = md.sine_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
      noise = md.white_noise(1024, amplitude=0.1, seed=42)
      mixed = md.mix(sine, noise, w_a=0.8, w_b=0.2)
