Spectrogram Text Art
====================

Synthesise audio that displays readable text when viewed as a spectrogram.

The function rasterises text with a built-in 5 × 7 bitmap font.  Each
bitmap column becomes a time slice; each "on" pixel becomes a sine wave at
the corresponding frequency between *freq_lo* and *freq_hi*.  A 3 ms
raised-cosine crossfade suppresses clicks at column boundaries.  The
output is normalised to 0.9 peak amplitude.

.. autofunction:: pyminidsp.spectrogram_text

   :param text: Printable ASCII string to render (must be non-empty).
   :param freq_lo: Lowest frequency in Hz (bottom of text).
   :param freq_hi: Highest frequency in Hz (top of text, must be < Nyquist).
   :param duration_sec: Total duration in seconds.
   :param sample_rate: Sample rate in Hz.
   :returns: Array of audio samples.

   .. code-block:: python

      sig = md.spectrogram_text("HELLO", freq_lo=200.0, freq_hi=7500.0,
                                 duration_sec=2.0, sample_rate=16000.0)
      # View the spectrogram of sig to see "HELLO" spelled out
