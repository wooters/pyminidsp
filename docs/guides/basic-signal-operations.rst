Basic Signal Operations
======================

Five fundamental time-domain analysis techniques that work alongside
:func:`~pyminidsp.energy`, :func:`~pyminidsp.power`, and
:func:`~pyminidsp.entropy`.


RMS (Root Mean Square)
----------------------

The standard measure of signal "loudness":

.. math::

   \text{RMS} = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} x[n]^2}

A unit sine wave yields ≈ 0.707; a DC signal of value *c* has RMS = |c|.

.. code-block:: python

   import pyminidsp as md

   signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)
   print(md.rms(signal))  # ≈ 0.707


Zero-crossing rate
------------------

Counts how often the signal changes sign, normalised by the number of
adjacent pairs.  High ZCR → noise or high-frequency content.  Low ZCR →
tonal or low-frequency content.

.. code-block:: python

   signal = md.sine_wave(16000, freq=1000.0, sample_rate=16000.0)
   zcr = md.zero_crossing_rate(signal)
   # zcr ≈ 2 * 1000 / 16000 = 0.125


Autocorrelation
---------------

Measures the similarity between a signal and a delayed copy of itself.
Periodic signals produce a strong peak at the fundamental period —
the basis of autocorrelation-based pitch detection.

.. code-block:: python

   signal = md.sine_wave(1024, freq=100.0, sample_rate=1000.0)
   acf = md.autocorrelation(signal, max_lag=50)
   # acf[0] = 1.0
   # acf[10] ≈ 1.0  (lag 10 = one period of 100 Hz at 1 kHz sample rate)


Peak detection
--------------

Finds local maxima above a threshold with a minimum distance constraint
to suppress secondary peaks.

.. code-block:: python

   import numpy as np

   signal = np.array([0, 1, 3, 1, 0, 2, 5, 2, 0], dtype=float)
   peaks = md.peak_detect(signal, threshold=0.0, min_distance=1)
   print(peaks)  # [2, 6]  (values 3 and 5)


Signal mixing
-------------

Element-wise weighted sum of two signals:

.. math::

   \text{out}[n] = w_a \cdot a[n] + w_b \cdot b[n]

.. code-block:: python

   sine = md.sine_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
   noise = md.white_noise(1024, amplitude=0.1, seed=42)
   mixed = md.mix(sine, noise, w_a=0.8, w_b=0.2)
