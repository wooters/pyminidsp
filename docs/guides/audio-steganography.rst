Audio Steganography
===================

Hide secret messages or binary data within audio signals so that casual
listeners hear only the original sound, while decoders can extract the
hidden payload.


Two methods
-----------

.. list-table::
   :header-rows: 1
   :widths: 12 18 18 27 25

   * - Method
     - Capacity
     - Audibility
     - Robustness
     - Requirement
   * - **LSB**
     - ~1 bit/sample (~16 KB / 3 s @ 44.1 kHz)
     - Inaudible (≈ −90 dB)
     - Fragile (destroyed by lossy compression, resampling)
     - Any sample rate
   * - **Frequency-band**
     - ~2.6 kbit/s (~121 bytes / 3 s @ 44.1 kHz)
     - Above most listeners' hearing
     - Moderate (survives mild noise)
     - sample_rate ≥ 40 kHz

**LSB** flips the least-significant bit of a 16-bit PCM representation —
distortion ≈ −90 dB.  Best for lossless pipelines (WAV, FLAC).

**Frequency-band** encodes data as brief BFSK tone bursts at 18.5 kHz
(bit 0) or 19.5 kHz (bit 1).  Choose this when light interference is
expected.


Message structure
-----------------

Both methods prepend a **32-bit little-endian header**: bits 0–30 hold
the byte count, bit 31 indicates payload type (0 = text, 1 = binary).
This lets the decoder recover messages without prior knowledge of length.


Hiding text
-----------

.. code-block:: python

   import pyminidsp as md

   host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
   stego, n = md.steg_encode(host, "secret message",
                              sample_rate=44100.0, method=md.STEG_LSB)
   print(f"Encoded {n} bytes")

**Listen** — compare the host signal and the stego outputs:

*Original host (440 Hz sine):*

.. raw:: html

   <audio controls style="margin: 0.5em 0;">
     <source src="../_static/audio/steg_host.wav" type="audio/wav">
     <em>Your browser does not support the audio element.</em>
   </audio>

*LSB-encoded (sounds identical):*

.. raw:: html

   <audio controls style="margin: 0.5em 0;">
     <source src="../_static/audio/steg_lsb.wav" type="audio/wav">
     <em>Your browser does not support the audio element.</em>
   </audio>

*Frequency-band encoded (faint high-frequency tones):*

.. raw:: html

   <audio controls style="margin: 0.5em 0;">
     <source src="../_static/audio/steg_freq.wav" type="audio/wav">
     <em>Your browser does not support the audio element.</em>
   </audio>


Recovering text
---------------

.. code-block:: python

   recovered = md.steg_decode(stego, sample_rate=44100.0, method=md.STEG_LSB)
   print(recovered)  # "secret message"


Binary data
-----------

.. code-block:: python

   data = b"\x00\x01\x02\xff\xfe\xfd"
   stego, n = md.steg_encode_bytes(host, data, sample_rate=44100.0)
   recovered = md.steg_decode_bytes(stego, sample_rate=44100.0)
   assert recovered == data


Automatic detection
-------------------

.. code-block:: python

   method, payload_type = md.steg_detect(stego, sample_rate=44100.0)
   if method is not None:
       print(f"Method: {'LSB' if method == md.STEG_LSB else 'Freq-band'}")
       print(f"Type: {'text' if payload_type == md.STEG_TYPE_TEXT else 'binary'}")


Capacity check
--------------

.. code-block:: python

   cap = md.steg_capacity(44100, sample_rate=44100.0, method=md.STEG_LSB)
   print(f"Can hide up to {cap} bytes")

   md.shutdown()
