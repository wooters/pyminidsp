FIR Filters & Convolution
=========================

Time-domain and FFT-based convolution, moving-average filters, and
general FIR filtering.

.. autofunction:: pyminidsp.convolution_num_samples

   Compute the output length of a full linear convolution.
   For input length *N* and kernel length *M*, the result is ``N + M - 1``.

.. autofunction:: pyminidsp.convolution_time

   Time-domain full linear convolution (direct sum-of-products).

   .. math::

      \text{out}[n] = \sum_{k=0}^{M-1} \text{signal}[n-k] \cdot \text{kernel}[k]

   with out-of-range signal samples treated as zero.

   :param signal: Input signal.
   :param kernel: FIR kernel.
   :returns: Array of length ``len(signal) + len(kernel) - 1``.

.. autofunction:: pyminidsp.moving_average

   Causal moving-average FIR filter with zero-padded startup.

   .. math::

      \text{out}[n] = \frac{1}{W} \sum_{k=0}^{W-1} \text{signal}[n-k]

   where out-of-range samples (``n - k < 0``) are treated as zero.

   :param signal: Input signal.
   :param window_len: Moving-average window length (must be > 0).
   :returns: Array of the same length as the input.

.. autofunction:: pyminidsp.fir_filter

   Apply a causal FIR filter with arbitrary coefficients.

   .. math::

      \text{out}[n] = \sum_{k=0}^{T-1} \text{coeffs}[k] \cdot \text{signal}[n-k]

   with out-of-range signal samples treated as zero.

   :param signal: Input signal.
   :param coeffs: FIR coefficients.
   :returns: Array of the same length as the input.

.. autofunction:: pyminidsp.convolution_fft_ola

   Full linear convolution using FFT overlap-add.  Produces the same
   output as :func:`convolution_time` but is faster for longer kernels
   by processing blocks in the frequency domain.

   :param signal: Input signal.
   :param kernel: FIR kernel.
   :returns: Array of length ``len(signal) + len(kernel) - 1``.
