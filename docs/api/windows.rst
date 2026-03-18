Window Functions
================

Window functions taper finite signal blocks before FFT processing to
prevent **spectral leakage** — the spreading of energy into neighbouring
frequency bins caused by discontinuities at block edges.

.. list-table:: Window comparison
   :header-rows: 1

   * - Window
     - Edge values
     - Sidelobe level
     - Main lobe width
   * - Rectangular
     - 1.0
     - Highest
     - Narrowest
   * - Hanning
     - 0.0
     - Low
     - Medium
   * - Hamming
     - 0.08
     - Lower first sidelobe
     - Medium
   * - Blackman
     - 0.0
     - Lowest
     - Widest
   * - Kaiser
     - configurable
     - configurable (via *beta*)
     - configurable (via *beta*)

Hanning is an effective default.  Blackman excels when minimising leakage
takes priority over frequency resolution.  Kaiser is the most flexible —
its *beta* parameter lets you dial in exact sidelobe/main-lobe trade-offs.

.. autofunction:: pyminidsp.hann_window

   Generate a Hanning (Hann) window:

   .. math::

      w[n] = 0.5\bigl(1 - \cos(2\pi n / (N-1))\bigr)

   Tapers to zero at both ends and is the default for FFT analysis.

.. autofunction:: pyminidsp.hamming_window

   Generate a Hamming window:

   .. math::

      w[n] = 0.54 - 0.46 \cos(2\pi n / (N-1))

   Similar to Hanning, but with a lower first sidelobe.

.. autofunction:: pyminidsp.blackman_window

   Generate a Blackman window:

   .. math::

      w[n] = 0.42 - 0.5\cos(2\pi n/(N-1)) + 0.08\cos(4\pi n/(N-1))

   Much lower sidelobes than Hanning/Hamming, with a wider main lobe.

.. autofunction:: pyminidsp.rect_window

   Generate a rectangular window (all ones).  Useful as a baseline
   reference — equivalent to no tapering.

.. autofunction:: pyminidsp.kaiser_window

   Generate a Kaiser window of length *n* with shape parameter *beta*.

   Unlike the other window functions, Kaiser windows take a *beta*
   parameter that controls the trade-off between main-lobe width and
   side-lobe level:

   - *beta* ≈ 5: similar to Hamming
   - *beta* ≈ 8.6: similar to Blackman
   - *beta* ≈ 14: very high sidelobe suppression

   .. math::

      w[n] = \frac{I_0\!\left(\beta\sqrt{1 - \left(\frac{2n}{N-1} - 1\right)^2}\right)}{I_0(\beta)}

   :param n: Window length.
   :param beta: Shape parameter.
   :returns: Array of length *n*.
