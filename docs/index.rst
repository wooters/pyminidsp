pyminidsp
=========

Python bindings to the `miniDSP <https://github.com/wooters/miniDSP>`_ C library.

A comprehensive DSP toolkit providing signal generation, spectral analysis,
filtering, effects, and more.  All functions accept and return
`NumPy <https://numpy.org>`_ arrays (``float64``).

These are the kinds of building blocks you'd use in an audio processing
pipeline — for example, estimating which direction a sound came from
using a pair of microphones.

.. code-block:: python

   import pyminidsp as md

   # Generate a 440 Hz sine wave (1 second at 44.1 kHz)
   signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)

   # Compute the magnitude spectrum
   mag = md.magnitude_spectrum(signal)

   # Apply a low-pass biquad filter
   lpf = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
   filtered = lpf.process_array(signal)

   # Clean up FFT caches when done
   md.shutdown()


.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   quickstart
   guides/index
   api/index
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
