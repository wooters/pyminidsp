Signal Generators
=================

pyminidsp provides stateless signal generators for creating test signals.
No audio input or microphone source is needed — just specify the
parameters and get a NumPy array back.

Sine wave
---------

The fundamental test signal — a pure tone at a single frequency:

.. math::

   x[n] = A \sin(2\pi f \, n / f_s)

.. code-block:: python

   import pyminidsp as md

   signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)

   # Verify: the FFT peak should align with the expected frequency bin
   mag = md.magnitude_spectrum(signal)


Impulse (Kronecker delta)
-------------------------

A single spike at a given position, zeros everywhere else.  The unit
impulse (amplitude 1.0 at position 0) is the identity element of
convolution and has a perfectly flat magnitude spectrum.

.. code-block:: python

   imp = md.impulse(1024, amplitude=1.0, position=0)

   # Flat spectrum — all bins have equal magnitude
   mag = md.magnitude_spectrum(imp)


Chirp (swept sine)
------------------

Two varieties:

**Linear chirp** — frequency sweeps at a constant rate.  The
instantaneous frequency traces a straight diagonal in the spectrogram.

.. code-block:: python

   # 1-second sweep from 200 Hz to 4 kHz at 16 kHz sample rate
   chirp = md.chirp_linear(16000, amplitude=1.0, f_start=200.0,
                            f_end=4000.0, sample_rate=16000.0)

**Logarithmic chirp** — exponential sweep, spending equal time per
octave.  Ideal for measuring systems on a log-frequency axis.

.. code-block:: python

   # Full audible range sweep: 20 Hz to 20 kHz
   chirp = md.chirp_log(44100, amplitude=1.0, f_start=20.0,
                         f_end=20000.0, sample_rate=44100.0)


Square wave
-----------

Alternates between +amplitude and −amplitude.  Its Fourier series
contains only **odd harmonics** (1f, 3f, 5f, …) with amplitudes
decaying as 1/k — a textbook demonstration of the Gibbs phenomenon.

.. code-block:: python

   sq = md.square_wave(4096, amplitude=1.0, freq=440.0, sample_rate=44100.0)


Sawtooth wave
-------------

Ramps linearly from −amplitude to +amplitude each period.  Contains
**all integer harmonics** (1f, 2f, 3f, …) decaying as 1/k — richer
harmonic content than the square wave's odd-only series.

.. code-block:: python

   saw = md.sawtooth_wave(4096, amplitude=1.0, freq=440.0, sample_rate=44100.0)


White noise
-----------

Gaussian white noise has equal power at all frequencies — its PSD is
approximately flat.  Samples follow N(0, σ²) via the Box-Muller
transform.  A fixed seed gives reproducible output.

.. code-block:: python

   noise = md.white_noise(4096, amplitude=1.0, seed=42)

   # Same seed → same output
   noise2 = md.white_noise(4096, amplitude=1.0, seed=42)
   assert (noise == noise2).all()


Shepard tone
------------

See :doc:`shepard-tone` for a dedicated guide on this auditory illusion.
