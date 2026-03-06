DTMF Tone Detection & Generation
=================================

`Dual-Tone Multi-Frequency (DTMF)
<https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling>`_ is
the signalling system used by touch-tone telephones.  Each keypad button
is encoded as a pair of sinusoids — one from a low-frequency "row" group
and one from a high-frequency "column" group:

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
false detections from speech.


Timing standards
----------------

`ITU-T Q.24 <https://www.itu.int/rec/T-REC-Q.24>`_ specifies:

- Minimum tone duration: **40 ms**
- Minimum inter-digit pause: **40 ms**

Practical systems typically use 70–120 ms for both.


Generating tones
----------------

.. code-block:: python

   import pyminidsp as md

   # Generate "5551234" at 8 kHz with 70 ms tones and pauses
   sig = md.dtmf_generate("5551234", sample_rate=8000.0, tone_ms=70, pause_ms=70)

Each digit is rendered as the sum of its row and column sinusoids at
amplitude 0.5 (peak combined amplitude = 1.0).

.. raw:: html

   <iframe src="../_static/plots/dtmf_spectrogram.html" style="width:100%;max-width:800px;height:380px;border:1px solid #ddd;border-radius:4px;margin:1em 0;" frameborder="0"></iframe>


Detecting tones
---------------

.. code-block:: python

   tones = md.dtmf_detect(sig, sample_rate=8000.0)
   for digit, start_s, end_s in tones:
       print(f"{digit}  {start_s:.3f}–{end_s:.3f} s")

Detection uses a sliding Hanning-windowed FFT with a state machine that
enforces ITU-T Q.24 minimum timing.  The FFT size is the largest power
of two fitting within 35 ms (e.g. 256 at 8 kHz, giving 31.25 Hz
resolution).


Round-trip verification
-----------------------

.. code-block:: python

   digits = "5551234"
   sig = md.dtmf_generate(digits, sample_rate=8000.0)
   detected = md.dtmf_detect(sig, sample_rate=8000.0)
   result = "".join(t[0] for t in detected)
   assert result == digits

   md.shutdown()
