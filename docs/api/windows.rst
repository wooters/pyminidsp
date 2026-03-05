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

Hanning is an effective default.  Blackman excels when minimising leakage
takes priority over frequency resolution.

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
