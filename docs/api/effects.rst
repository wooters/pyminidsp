Simple Effects
==============

Delay-line based audio effects: echo, tremolo, and comb-filter reverb.

.. autofunction:: pyminidsp.delay_echo

   Delay line / echo effect using a circular buffer with feedback.
   Creates repeating echoes that decay geometrically when
   ``|feedback| < 1``.

   Internal delay state:

   .. math::

      s[n] = x[n] + \text{feedback} \cdot s[n - D]

   Output:

   .. math::

      y[n] = \text{dry} \cdot x[n] + \text{wet} \cdot s[n - D]

   :param signal: Input signal.
   :param delay_samples: Delay length in samples (must be > 0).
   :param feedback: Echo feedback gain (must satisfy ``|feedback| < 1``).
   :param dry: Dry (original) mix weight.
   :param wet: Wet (delayed) mix weight.
   :returns: Processed signal (same length as input).

.. autofunction:: pyminidsp.tremolo

   Tremolo effect — amplitude modulation by a sinusoidal LFO.

   The modulation gain is:

   .. math::

      g[n] = (1 - d) + d \cdot \frac{1 + \sin(2\pi f_\text{LFO} \, n / f_s)}{2}

   so ``g[n]`` ranges from ``1 - depth`` to ``1``.

   :param signal: Input signal.
   :param rate_hz: LFO rate in Hz (must be >= 0).
   :param depth: Modulation depth in [0, 1].
   :param sample_rate: Sampling rate in Hz.
   :returns: Processed signal (same length as input).

.. autofunction:: pyminidsp.comb_reverb

   Comb-filter reverb (feedback comb filter with dry/wet mix).

   Internal comb section:

   .. math::

      c[n] = x[n] + \text{feedback} \cdot c[n - D]

   Output:

   .. math::

      y[n] = \text{dry} \cdot x[n] + \text{wet} \cdot c[n]

   :param signal: Input signal.
   :param delay_samples: Comb delay in samples (must be > 0).
   :param feedback: Feedback gain (must satisfy ``|feedback| < 1``).
   :param dry: Dry (original) mix weight.
   :param wet: Wet (comb output) mix weight.
   :returns: Processed signal (same length as input).
