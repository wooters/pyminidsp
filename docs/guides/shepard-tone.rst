Shepard Tone
============

A `Shepard tone <https://en.wikipedia.org/wiki/Shepard_tone>`_ is an
acoustic illusion — a sound that appears to continuously rise (or fall)
in pitch without ever actually leaving its frequency range.  Cognitive
scientist Roger Shepard first described this effect in 1964.  It mirrors
an M.C. Escher staircase: listeners perceive endless ascending motion
that never reaches its destination.


How it works
------------

The illusion relies on two principles:

1. **Octave equivalence** — the human ear perceives tones one octave
   apart as the "same note" at a different pitch height.
2. **Spectral envelope** — a fixed Gaussian curve in log-frequency space
   controls loudness.  Tones near the centre are loud; those at edges
   fade nearly silent.

Multiple sine waves — each separated by one octave — sound
simultaneously while gliding upward.  As tones fade at the upper edge,
new tones enter at the bottom, fading in.  The loudest tones always
occupy the middle and move upward, so the sound seems to ascend
perpetually.


Signal model
------------

.. math::

   x[n] = A_\text{norm}\sum_k
     \exp\!\left(-\frac{d_k(t)^2}{2\sigma^2}\right)
     \sin(\varphi_k(n))

where the octave distance from the Gaussian centre is

.. math::

   d_k(t) = k - c + R\,t, \quad
   c = \frac{L-1}{2}, \quad
   \sigma = \frac{L}{4}

and the instantaneous frequency of layer *k* is
:math:`f_k(t) = f_\text{base} \cdot 2^{d_k(t)}`.  Phase is accumulated
sample-by-sample for smooth glides.


Example
-------

.. code-block:: python

   import pyminidsp as md

   # 5 seconds of endlessly rising Shepard tone at 44.1 kHz
   sig = md.shepard_tone(5 * 44100, amplitude=0.8, base_freq=440.0,
                          sample_rate=44100.0, rate_octaves_per_sec=0.5,
                          num_octaves=8)

**Listen** — rising Shepard tone (5 seconds):

.. raw:: html

   <audio controls style="margin: 0.5em 0;">
     <source src="../_static/audio/shepard_rising.wav" type="audio/wav">
     <em>Your browser does not support the audio element.</em>
   </audio>

   <iframe src="../_static/plots/shepard_rising_spectrogram.html" style="width:100%;max-width:800px;height:380px;border:1px solid #ddd;border-radius:4px;margin:1em 0;" frameborder="0"></iframe>

**Falling** Shepard tone:

.. raw:: html

   <audio controls style="margin: 0.5em 0;">
     <source src="../_static/audio/shepard_falling.wav" type="audio/wav">
     <em>Your browser does not support the audio element.</em>
   </audio>

   <iframe src="../_static/plots/shepard_falling_spectrogram.html" style="width:100%;max-width:800px;height:380px;border:1px solid #ddd;border-radius:4px;margin:1em 0;" frameborder="0"></iframe>

**Static** chord (rate = 0):

.. raw:: html

   <audio controls style="margin: 0.5em 0;">
     <source src="../_static/audio/shepard_static.wav" type="audio/wav">
     <em>Your browser does not support the audio element.</em>
   </audio>


Key parameters
--------------

**Glissando rate** (``rate_octaves_per_sec``):

- ``0.0`` — static chord (no motion)
- ``0.5`` — moderate rise (default)
- Negative values → falling Shepard tone

**Number of octaves** (``num_octaves``):

- 4–6 — narrow, organ-like quality
- 8 — balanced (default)
- 10–12 — ethereal, diffuse texture

**Base frequency** (``base_freq``): centres the Gaussian envelope.
Typical values: 200–600 Hz.

.. code-block:: python

   # Slowly falling Shepard tone
   falling = md.shepard_tone(44100 * 3, amplitude=0.8, base_freq=300.0,
                              sample_rate=44100.0, rate_octaves_per_sec=-0.3,
                              num_octaves=10)

   md.shutdown()
