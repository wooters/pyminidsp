Audio Steganography
===================

Hide secret messages or binary data within audio signals so that casual
listeners hear only the original sound.

Three methods are provided:

.. list-table::
   :header-rows: 1
   :widths: 15 20 20 25 20

   * - Method
     - Capacity
     - Audibility
     - Robustness
     - Requirement
   * - **LSB** (:data:`STEG_LSB`)
     - ~1 bit/sample (~16 KB per 3 s at 44.1 kHz)
     - Inaudible (≈ −90 dB)
     - Fragile (destroyed by lossy compression)
     - Any sample rate
   * - **Frequency-band** (:data:`STEG_FREQ_BAND`)
     - ~2.6 kbit/s (~121 bytes per 3 s at 44.1 kHz)
     - Above most listeners' hearing range
     - Moderate (survives mild noise)
     - sample_rate ≥ 40 kHz
   * - **Spectrogram text** (:data:`STEG_SPECTEXT`)
     - ~1 bit/sample (same as LSB)
     - Audible as buzzy tones; visually readable in spectrogram
     - Fragile (same as LSB)
     - Any sample rate

All methods prepend a 32-bit length header so the decoder can recover
the message without knowing its length in advance.

.. autofunction:: pyminidsp.steg_capacity

   Compute the maximum message length (in bytes) that can be hidden.

.. autofunction:: pyminidsp.steg_encode

   Encode a secret text message into a host audio signal.

   - **LSB** — flips the least-significant bit of a 16-bit PCM
     representation.  Distortion ≈ −90 dB.
   - **Frequency-band** — adds a low-amplitude BFSK tone in the
     near-ultrasonic band (18.5 / 19.5 kHz).
   - **Spectrogram text** — hybrid LSB encoding that also renders the
     message as readable text in a spectrogram view.

   :param host: Host signal (not modified).
   :param message: String message to hide.
   :param sample_rate: Sample rate in Hz.
   :param method: :data:`STEG_LSB`, :data:`STEG_FREQ_BAND`, or :data:`STEG_SPECTEXT`.
   :returns: ``(stego_signal, num_bytes_encoded)`` tuple.

   .. code-block:: python

      host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
      stego, n = md.steg_encode(host, "secret", sample_rate=44100.0, method=md.STEG_LSB)

.. autofunction:: pyminidsp.steg_decode

   Decode a secret text message from a stego audio signal.

   :returns: Decoded string message (empty string if none found).

.. autofunction:: pyminidsp.steg_encode_bytes

   Encode arbitrary binary data (may contain null bytes — e.g. images,
   compressed archives, cryptographic keys).

   :param host: Host signal.
   :param data: Bytes-like object to hide.
   :param sample_rate: Sample rate in Hz.
   :param method: :data:`STEG_LSB`, :data:`STEG_FREQ_BAND`, or :data:`STEG_SPECTEXT`.
   :returns: ``(stego_signal, num_bytes_encoded)`` tuple.

.. autofunction:: pyminidsp.steg_decode_bytes

   Decode binary data from a stego audio signal.

   :returns: ``bytes`` object containing the decoded data.

.. autofunction:: pyminidsp.steg_detect

   Detect which steganography method (if any) was used.

   Probes the signal for a valid header using all three methods (LSB,
   frequency-band, and spectrogram text).  If multiple appear valid,
   frequency-band is preferred (lower false-positive rate).

   :returns: ``(method, payload_type)`` tuple, or ``(None, None)`` if no
             steganographic content is detected.
