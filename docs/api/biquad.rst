Biquad Filter
=============

Second-order IIR (biquad) filter supporting seven filter types.  Based
on the `Audio EQ Cookbook <https://www.w3.org/2011/audio/audio-eq-cookbook.html>`_
by Robert Bristow-Johnson.

Transfer function:

.. math::

   H(z) = \frac{b_0 + b_1 z^{-1} + b_2 z^{-2}}{a_0 + a_1 z^{-1} + a_2 z^{-2}}

Only five multiplications and four additions per sample, making it
efficient for real-time audio.

Filter types
------------

.. list-table::
   :header-rows: 1

   * - Constant
     - Type
     - Description
   * - :data:`LPF`
     - Low-pass
     - Passes frequencies below the cutoff
   * - :data:`HPF`
     - High-pass
     - Passes frequencies above the cutoff
   * - :data:`BPF`
     - Band-pass
     - Passes frequencies near the centre frequency
   * - :data:`NOTCH`
     - Notch
     - Rejects frequencies near the centre frequency
   * - :data:`PEQ`
     - Peaking EQ
     - Boost or cut at the centre frequency
   * - :data:`LSH`
     - Low shelf
     - Boost or cut all frequencies below the cutoff
   * - :data:`HSH`
     - High shelf
     - Boost or cut all frequencies above the cutoff

.. autoclass:: pyminidsp.BiquadFilter
   :members:
   :undoc-members:

   .. code-block:: python

      # Low-pass at 1 kHz, process a full signal
      lpf = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
      filtered = lpf.process_array(signal)

      # Peaking EQ: +6 dB at 3 kHz
      eq = md.BiquadFilter(md.PEQ, freq=3000.0, sample_rate=44100.0, db_gain=6.0)

      # Sample-by-sample processing
      for sample in signal:
          out = lpf.process(sample)
