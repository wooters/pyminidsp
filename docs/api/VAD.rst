Voice Activity Detection
========================

Frame-level voice activity detection with adaptive feature normalization
and onset/hangover smoothing.

The detector extracts five features per frame:

.. list-table::
   :header-rows: 1

   * - Index
     - Feature
   * - 0
     - Energy
   * - 1
     - Zero-crossing rate
   * - 2
     - Spectral entropy
   * - 3
     - Spectral flatness
   * - 4
     - Band energy ratio

Features are normalized to [0.0, 1.0] using adaptive EMA tracking, then
combined into a weighted score:

.. math::

   S = \sum_{i=0}^{4} w_i \cdot \hat{f}_i

An onset/hangover state machine smooths the final decision.

.. autoclass:: pyminidsp.VAD
   :members:
   :undoc-members:

   .. code-block:: python

      import pyminidsp as md

      detector = md.VAD(threshold=0.4)

      # Calibrate with silence
      silence = md.white_noise(320, amplitude=0.0, seed=0)
      for _ in range(10):
          detector.calibrate(silence, sample_rate=16000.0)

      # Process a single frame
      frame = md.sine_wave(320, amplitude=1.0, freq=1000.0, sample_rate=16000.0)
      decision, score, features = detector.process_frame(frame, 16000.0)

      # Batch-process an entire signal
      signal = md.sine_wave(16000, amplitude=1.0, freq=1000.0, sample_rate=16000.0)
      decisions, scores, features = detector.process(signal, 16000.0, frame_len=320)

.. data:: pyminidsp.VAD_NUM_FEATURES

   Number of features extracted per frame (5).
