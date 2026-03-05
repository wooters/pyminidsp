Mel Filterbanks & MFCCs
=======================

Two essential features for speech and audio machine learning:

1. **Mel filterbank energies** — triangular spectral bands spaced on the
   `mel scale <https://en.wikipedia.org/wiki/Mel_scale>`_, which
   compresses frequency representation to match human hearing.
2. **MFCCs** — decorrelated coefficients derived from the log mel
   energies via a DCT, widely used in speech recognition and audio
   classification.


Mel scale
---------

The HTK mapping:

.. math::

   \text{mel}(f) = 2595 \cdot \log_{10}\!\left(1 + \frac{f}{700}\right)

This densifies low frequencies and coarsens high frequencies, reflecting
how humans perceive pitch.


Building a mel filterbank
-------------------------

.. code-block:: python

   import pyminidsp as md

   fb = md.mel_filterbank(512, sample_rate=16000.0, num_mels=26)
   # fb.shape == (26, 257)  — 26 triangular filters over 257 FFT bins


Computing mel energies
----------------------

From a single frame:

.. code-block:: python

   signal = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
   mel = md.mel_energies(signal, sample_rate=16000.0, num_mels=26)
   # mel.shape == (26,)

Processing steps (internally):

1. Apply a Hann window.
2. Compute one-sided PSD bins via FFT: ``|X(k)|² / N``.
3. Apply mel filterbank weights and sum per band.


Computing MFCCs
---------------

.. code-block:: python

   coeffs = md.mfcc(signal, sample_rate=16000.0, num_mels=26, num_coeffs=13)
   # coeffs.shape == (13,)

Conventions:

- HTK mel mapping for filter placement.
- Natural-log compression: ``log(max(E_mel, 1e-12))``.
- DCT-II with HTK-C0 normalisation.
- Coefficient C0 is in ``coeffs[0]``.


Processing a full utterance
---------------------------

To extract MFCCs from a longer signal, use the STFT to break it into
frames first:

.. code-block:: python

   import numpy as np

   sr = 16000.0
   frame_size = 512
   hop = 128

   # Load or generate a signal
   signal = md.chirp_linear(int(sr), f_start=200.0, f_end=4000.0, sample_rate=sr)

   num_frames = md.stft_num_frames(len(signal), frame_size, hop)
   all_mfcc = np.zeros((num_frames, 13))
   for f in range(num_frames):
       start = f * hop
       frame = signal[start:start + frame_size]
       all_mfcc[f] = md.mfcc(frame, sample_rate=sr, num_mels=26, num_coeffs=13)

   md.shutdown()
