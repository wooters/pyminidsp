FIR Filters & Convolution
=========================

Four complementary methods for filtering and convolution, from
educational time-domain approaches to efficient FFT-based processing.


Time-domain convolution
-----------------------

For signals of length *N* and kernels of length *M*, computes the full
linear convolution.  Output length is ``N + M - 1``.

.. code-block:: python

   import pyminidsp as md
   import numpy as np

   signal = md.impulse(100, amplitude=1.0, position=0)
   kernel = np.array([1.0, 2.0, 3.0])
   out = md.convolution_time(signal, kernel)
   # out[:3] == [1.0, 2.0, 3.0]
   # len(out) == 102


Moving-average filter
---------------------

A simple low-pass filter that computes the running mean over a window.
Output matches input length with zero-padded startup.

.. code-block:: python

   signal = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
   smoothed = md.moving_average(signal, window_len=5)


General FIR filter
------------------

Apply a causal FIR filter with arbitrary coefficients:

.. math::

   \text{out}[n] = \sum_{k=0}^{T-1} \text{coeffs}[k] \cdot \text{signal}[n-k]

Output matches input length.

.. code-block:: python

   coeffs = np.array([0.25, 0.5, 0.25])
   filtered = md.fir_filter(signal, coeffs)


FFT overlap-add
---------------

Same result as time-domain convolution but **much faster for long
kernels** by processing blocks in the frequency domain.

.. code-block:: python

   kernel = md.hann_window(256)
   out_time = md.convolution_time(signal, kernel)
   out_fft = md.convolution_fft_ola(signal, kernel)
   np.testing.assert_allclose(out_time, out_fft, atol=1e-10)


Comparison
----------

.. list-table::
   :header-rows: 1

   * - Method
     - Complexity
     - Output length
     - Best for
   * - ``convolution_time``
     - O(NM)
     - N + M − 1
     - Teaching, short kernels
   * - ``moving_average``
     - O(N)
     - N
     - Simple smoothing
   * - ``fir_filter``
     - O(NM)
     - N
     - Standard FIR design
   * - ``convolution_fft_ola``
     - O(N log N)
     - N + M − 1
     - Long kernels, production

.. code-block:: python

   md.shutdown()
