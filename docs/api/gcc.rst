Delay Estimation (GCC-PHAT)
===========================

Generalized Cross-Correlation for estimating the time delay between
two microphone signals that captured the same sound source.  This is
the basis of acoustic source localisation.

**Algorithm:**

1. FFT both signals.
2. Multiply one spectrum by the conjugate of the other (cross-spectrum).
3. Apply a weighting (PHAT normalises by magnitude, sharpening the peak).
4. Inverse-FFT back to the time domain.
5. The position of the peak tells you the delay in samples.

.. autofunction:: pyminidsp.get_delay

   Estimate the delay between two signals.

   :param sig_a: First signal.
   :param sig_b: Second signal.
   :param margin: Search ± this many samples around zero-lag.
   :param weighting: :data:`GCC_SIMP` or :data:`GCC_PHAT`.
   :returns: ``(delay, entropy)`` tuple.  *delay* is in samples (positive =
             *sig_b* lags *sig_a*).  *entropy* is normalised entropy of the
             correlation peak region (closer to 1.0 = less trustworthy).

   .. code-block:: python

      import numpy as np
      sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
      sig_b = np.roll(sig_a, 5)
      delay, ent = md.get_delay(sig_a, sig_b, margin=20, weighting=md.GCC_PHAT)
      # delay == 5

.. autofunction:: pyminidsp.get_multiple_delays

   Estimate delays between a reference signal and M − 1 other signals.

   :param signals: List of arrays (``signals[0]`` is the reference).
   :param margin: Search window in samples.
   :param weighting: :data:`GCC_SIMP` or :data:`GCC_PHAT`.
   :returns: Array of ``M - 1`` delay values.

.. autofunction:: pyminidsp.gcc

   Compute the full generalized cross-correlation between two signals.

   :param sig_a: First signal.
   :param sig_b: Second signal.
   :param weighting: :data:`GCC_SIMP` or :data:`GCC_PHAT`.
   :returns: Array of *N* doubles.  The zero-lag value is at index
             ``ceil(N / 2)``.
