Simple Audio Effects
====================

Three foundational audio effects built on delay lines.


Delay / echo
-------------

A circular buffer with feedback creates repeating echoes that decay
geometrically:

.. math::

   s[n] &= x[n] + \text{feedback} \cdot s[n - D] \\
   y[n] &= \text{dry} \cdot x[n] + \text{wet} \cdot s[n - D]

.. code-block:: python

   import pyminidsp as md

   signal = md.sine_wave(44100, freq=440.0, sample_rate=44100.0)
   echoed = md.delay_echo(signal, delay_samples=4410,
                           feedback=0.5, dry=1.0, wet=0.5)


Tremolo
-------

Amplitude modulation by a sinusoidal LFO.  The gain oscillates between
``1 - depth`` and ``1``:

.. math::

   g[n] = (1 - d) + d \cdot \frac{1 + \sin(2\pi f_\text{LFO} n / f_s)}{2}

.. code-block:: python

   tremmed = md.tremolo(signal, rate_hz=5.0, depth=0.5, sample_rate=44100.0)


Comb-filter reverb
------------------

Feeds delayed output back into itself, creating closely-spaced echoes
that simulate reverberation:

.. math::

   c[n] &= x[n] + \text{feedback} \cdot c[n - D] \\
   y[n] &= \text{dry} \cdot x[n] + \text{wet} \cdot c[n]

.. code-block:: python

   reverbed = md.comb_reverb(signal, delay_samples=1000,
                              feedback=0.5, dry=1.0, wet=0.3)


Verification tips
-----------------

- **Impulse response:** feed an impulse through each effect.  Echoes
  should decay predictably based on the feedback value.
- **Parameter extremes:** ``depth=0`` for tremolo should return the
  original signal unchanged.
- **Feedback = 0:** all effects should produce a single delayed copy
  (no ringing).

.. code-block:: python

   md.shutdown()
