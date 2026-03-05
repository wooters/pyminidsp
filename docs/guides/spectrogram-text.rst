Spectrogram Text Art
====================

Synthesise audio that displays **readable text** when viewed as a
spectrogram — time runs horizontally, frequency vertically.


How it works
------------

1. Each ASCII character (32–126) is rasterised with a built-in 5 × 7
   bitmap font, spaced 3 columns apart.
2. Each bitmap column becomes a time slice.
3. Each "on" pixel becomes a sine wave at the corresponding frequency
   between *freq_lo* and *freq_hi* (top row → highest frequency,
   bottom row → lowest, linearly interpolated).
4. A 3 ms raised-cosine crossfade at column boundaries suppresses
   clicks.
5. The output is normalised to 0.9 peak amplitude.


Example
-------

.. code-block:: python

   import pyminidsp as md

   sig = md.spectrogram_text("HELLO", freq_lo=200.0, freq_hi=7500.0,
                              duration_sec=2.0, sample_rate=16000.0)

   # View the spectrogram of `sig` to see "HELLO" spelled out
   # in the frequency domain.

The result sounds like a buzzy chord, but when analysed with a
spectrogram viewer (1024-point FFT at 16 kHz), the text is clearly
visible.


Tips
----

- Use a sample rate of at least 16 kHz and keep *freq_hi* below
  Nyquist.
- Longer *duration_sec* stretches the text horizontally — easier to
  read in spectrograms.
- Short strings work best (the 5 × 7 font has limited resolution).

.. code-block:: python

   md.shutdown()
