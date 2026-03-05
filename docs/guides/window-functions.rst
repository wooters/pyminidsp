Window Functions
================

Window functions taper finite signal blocks before FFT processing to
prevent **spectral leakage** — the spreading of energy into neighbouring
frequency bins caused by discontinuities at block edges.

The DFT assumes the input is one period of a periodic signal.  When the
signal doesn't have an integer number of cycles in the block, the
endpoints are mismatched.  A window smoothly tapers the signal to zero
at the edges, greatly reducing this leakage.


Four window types
-----------------

**Hanning (Hann)** — the default choice for FFT analysis.

.. math::

   w[n] = 0.5\bigl(1 - \cos(2\pi n / (N-1))\bigr)

.. code-block:: python

   import pyminidsp as md
   win = md.hann_window(256)

**Hamming** — similar to Hanning but with a lower first sidelobe.

.. math::

   w[n] = 0.54 - 0.46\cos(2\pi n / (N-1))

.. code-block:: python

   win = md.hamming_window(256)

**Blackman** — strongest sidelobe suppression, widest main lobe.

.. math::

   w[n] = 0.42 - 0.5\cos(2\pi n/(N-1)) + 0.08\cos(4\pi n/(N-1))

.. code-block:: python

   win = md.blackman_window(256)

**Rectangular** — all ones (no tapering).  Narrowest main lobe but
maximum sidelobe leakage.

.. code-block:: python

   win = md.rect_window(256)


Comparison
----------

.. list-table::
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

**Rule of thumb:** start with Hanning.  Use Blackman when minimising
leakage matters more than frequency resolution.
