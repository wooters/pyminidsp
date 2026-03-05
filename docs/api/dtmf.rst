DTMF
====

Dual-Tone Multi-Frequency (DTMF) tone generation and detection.

DTMF is the signalling system used by touch-tone telephones.  Each
keypad button is encoded as a pair of sinusoids — one from a
low-frequency "row" group and one from a high-frequency "column" group:

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - 1209 Hz
     - 1336 Hz
     - 1477 Hz
     - 1633 Hz
   * - 697 Hz
     - 1
     - 2
     - 3
     - A
   * - 770 Hz
     - 4
     - 5
     - 6
     - B
   * - 852 Hz
     - 7
     - 8
     - 9
     - C
   * - 941 Hz
     - \*
     - 0
     - #
     - D

The frequencies were chosen to avoid harmonic relationships, preventing
false detections from speech or other complex signals.

Timing follows `ITU-T Q.24 <https://www.itu.int/rec/T-REC-Q.24>`_:
minimum 40 ms tone-on, minimum 40 ms inter-digit pause.

.. autofunction:: pyminidsp.dtmf_signal_length

   Calculate the number of samples needed for :func:`dtmf_generate`:

   .. math::

      N = D \cdot \lfloor t_\text{tone} \cdot f_s / 1000 \rfloor
        + (D - 1) \cdot \lfloor t_\text{pause} \cdot f_s / 1000 \rfloor

.. autofunction:: pyminidsp.dtmf_generate

   Generate a DTMF tone sequence.  Each digit is rendered as the sum of
   its row and column sinusoids, each at amplitude 0.5 (peak sum = 1.0).

   :param digits: String of DTMF characters (``'0'``–``'9'``,
                  ``'A'``–``'D'``, ``'*'``, ``'#'``).
   :param sample_rate: Sampling rate in Hz.
   :param tone_ms: Duration of each tone in ms (>= 40).
   :param pause_ms: Duration of silence between tones in ms (>= 40).
   :returns: Array of audio samples.

   .. code-block:: python

      sig = md.dtmf_generate("5551234", sample_rate=8000.0)

.. autofunction:: pyminidsp.dtmf_detect

   Detect DTMF tones in an audio signal.

   Uses a sliding Hanning-windowed FFT with a state machine that
   enforces ITU-T Q.24 minimum timing constraints (40 ms tone-on,
   40 ms inter-digit pause).

   :param signal: Audio samples (mono).
   :param sample_rate: Sampling rate in Hz (must be >= 4000).
   :param max_tones: Maximum number of tones to detect.
   :returns: List of ``(digit, start_s, end_s)`` tuples.

   .. code-block:: python

      digits = "5551234"
      sig = md.dtmf_generate(digits, sample_rate=8000.0)
      tones = md.dtmf_detect(sig, sample_rate=8000.0)
      detected = "".join(t[0] for t in tones)
      assert detected == digits
