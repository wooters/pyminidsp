Voice Activity Detection
========================

`Voice activity detection (VAD)
<https://en.wikipedia.org/wiki/Voice_activity_detection>`_ is the task of
determining whether an audio frame contains speech or silence.  It is a
fundamental building block in speech processing pipelines — from automatic
speech recognition to noise-aware audio analysis.

pyminidsp provides a frame-level VAD that extracts five features per frame,
normalizes them adaptively, computes a weighted score, and applies an
onset/hangover state machine.


Features
--------

The detector extracts five features from each audio frame:

**Energy** — sum of squared samples.  Silence has near-zero energy; speech
has high energy.  Energy alone fails in moderate noise.

.. math::

   E = \sum_{n=0}^{N-1} x[n]^{2}

**Zero-crossing rate (ZCR)** — fraction of consecutive samples that cross
zero.  Voiced speech has low ZCR; unvoiced fricatives have high ZCR;
silence has low ZCR.

.. math::

   \text{ZCR} = \frac{1}{N-1} \sum_{n=1}^{N-1}
   \mathbf{1}\!\bigl[\operatorname{sgn}(x[n]) \neq \operatorname{sgn}(x[n-1])\bigr]

**Spectral entropy** — how spread out the energy is across frequency bins.
Speech has lower spectral entropy (energy concentrated in harmonics);
noise has higher spectral entropy (energy spread evenly).

.. math::

   H = -\frac{1}{\ln K} \sum_{k=0}^{K-1} p_k \ln p_k
   \qquad\text{where } p_k = \frac{\text{PSD}[k]}{\sum_j \text{PSD}[j]}

**Spectral flatness** — ratio of the geometric mean to the arithmetic
mean of the power spectrum.  White noise gives SF ≈ 1; a pure tone gives
SF ≈ 0.  Speech falls between.

.. math::

   \text{SF}
   = \frac{\bigl(\prod_{k=0}^{K-1} \text{PSD}[k]\bigr)^{1/K}}
          {\frac{1}{K}\sum_{k=0}^{K-1} \text{PSD}[k]}

**Band energy ratio** — fraction of total energy that falls within the
speech band (default 300–3400 Hz, telephone bandwidth).

.. math::

   \text{BER}
   = \frac{\sum_{k:\,f_k \in [f_\text{lo},\,f_\text{hi}]} \text{PSD}[k]}
          {\sum_k \text{PSD}[k]}


Adaptive normalization
----------------------

Raw feature values vary widely across recordings.  The detector tracks
per-feature minimums and maximums using an exponential moving average
(EMA) and normalizes each feature to [0, 1]:

.. math::

   m_i \leftarrow m_i + \alpha\,(f_i - m_i)
   \qquad
   M_i \leftarrow M_i + \alpha\,(f_i - M_i)

.. math::

   \hat{f}_i = \text{clamp}\!\Bigl(\frac{f_i - m_i}{M_i - m_i},\; 0,\; 1\Bigr)

The adaptation rate α (default 0.01) controls how fast the normalization
adjusts.  Calling :meth:`~pyminidsp.VAD.calibrate` with known silence
seeds the EMA estimates for faster convergence.


Weighted scoring
----------------

The five normalized features are combined into a single score:

.. math::

   S = \sum_{i=0}^{4} w_i \cdot \hat{f}_i

By default all weights are equal (0.2 each).  You can emphasize specific
features — for example, weighting energy heavily for clean environments,
or spectral entropy for noisy ones.


State machine
-------------

A raw score above the threshold does not immediately trigger speech.  An
onset/hangover state machine smooths the decision:

.. list-table::
   :header-rows: 1

   * - Current State
     - Condition
     - Action
   * - SILENCE
     - score ≥ threshold
     - Increment onset counter
   * - SILENCE
     - onset counter ≥ ``onset_frames``
     - Transition to SPEECH
   * - SILENCE
     - score < threshold
     - Reset onset counter
   * - SPEECH
     - score ≥ threshold
     - Reset hangover counter to ``hangover_frames``
   * - SPEECH
     - score < threshold
     - Decrement hangover counter
   * - SPEECH
     - hangover counter reaches 0
     - Transition to SILENCE

**Onset gating** prevents transient clicks from triggering false
positives — the score must exceed the threshold for ``onset_frames``
consecutive frames (default 3).

**Hangover** bridges brief dips mid-utterance, holding the speech state
for ``hangover_frames`` frames (default 15) after activity drops.


Creating a detector
-------------------

The :class:`~pyminidsp.VAD` class wraps the stateful C implementation.
All parameters are optional — omitted values use sensible defaults.

.. code-block:: python

   import pyminidsp as md

   # Default parameters
   detector = md.VAD()

   # Custom threshold and hangover
   detector = md.VAD(threshold=0.4, hangover_frames=20)

   # Custom feature weights (energy, ZCR, spectral entropy,
   # spectral flatness, band energy ratio)
   detector = md.VAD(weights=[0.4, 0.1, 0.1, 0.1, 0.3])


Calibrating with silence
-------------------------

Before processing live audio, feed a few frames of known silence to seed
the adaptive normalization.  This improves accuracy, especially in the
first few frames.

.. code-block:: python

   sr = 16000.0
   frame_len = 320  # 20 ms at 16 kHz
   silence = np.zeros(frame_len)

   for _ in range(10):
       detector.calibrate(silence, sample_rate=sr)


Frame-by-frame processing
--------------------------

:meth:`~pyminidsp.VAD.process_frame` processes a single frame and returns
a ``(decision, score, features)`` tuple.

.. code-block:: python

   frame = md.sine_wave(frame_len, amplitude=1.0, freq=1000.0, sample_rate=sr)

   decision, score, features = detector.process_frame(frame, sr)

   print(f"Decision: {'speech' if decision else 'silence'}")
   print(f"Score:    {score:.3f}")
   print(f"Features: {features}")

- **decision** — ``1`` for speech, ``0`` for silence.
- **score** — weighted combination of normalized features in [0.0, 1.0].
- **features** — float64 array of length 5 with normalized feature values.


Batch processing
----------------

:meth:`~pyminidsp.VAD.process` segments a signal into non-overlapping
frames and processes each one, returning arrays.

.. code-block:: python

   # 1 second of signal at 16 kHz
   signal = md.sine_wave(16000, amplitude=1.0, freq=1000.0, sample_rate=sr)

   decisions, scores, features = detector.process(signal, sr, frame_len=320)

   print(f"Frames processed: {len(decisions)}")
   print(f"Speech frames:    {decisions.sum()}")
   print(f"Features shape:   {features.shape}")  # (50, 5)


End-to-end example
------------------

The following example creates a synthetic signal with two speech-like
bursts separated by silence, runs the VAD, and prints per-frame results:

.. code-block:: python

   import numpy as np
   import pyminidsp as md

   sr = 16000.0
   frame_len = 320  # 20 ms

   # Build signal: silence → tone → silence → tone → silence
   seg = int(0.3 * sr)  # 300 ms segments
   signal = np.concatenate([
       np.zeros(seg),
       md.sine_wave(seg, amplitude=0.8, freq=1000.0, sample_rate=sr),
       np.zeros(seg),
       md.sine_wave(seg, amplitude=0.8, freq=1000.0, sample_rate=sr),
       np.zeros(seg),
   ])

   detector = md.VAD()

   # Calibrate with leading silence
   for i in range(10):
       frame = signal[i * frame_len:(i + 1) * frame_len]
       detector.calibrate(frame, sample_rate=sr)

   # Process
   decisions, scores, features = detector.process(signal, sr, frame_len)

   for i in range(len(decisions)):
       t = (i * frame_len + frame_len / 2) / sr
       label = "SPEECH" if decisions[i] else "silence"
       print(f"  {t:6.3f} s  score={scores[i]:.3f}  {label}")


Visualisation
-------------

The interactive plot below shows the VAD processing the synthetic signal
from the example above.  Four panels display: the per-frame peak
envelope, all five normalized features, the combined score against the
threshold (dashed red line), and the final binary decision.

.. raw:: html

   <iframe src="../_static/plots/vad_visualization.html"
           style="width:100%;max-width:900px;height:720px;border:1px solid #ddd;border-radius:4px;margin:1em 0;"
           frameborder="0"></iframe>


Tuning parameters
-----------------

The default parameters work well for clean speech at 16 kHz.  For noisy
environments, you may need to adjust:

- **threshold** (default 0.5) — lower values increase sensitivity.
- **onset_frames** (default 3) — more frames needed to confirm speech.
- **hangover_frames** (default 15) — how long to hold the speech state
  after activity drops.
- **adaptation_rate** (default 0.01) — EMA learning rate for
  normalization.  Lower values track slower-changing environments.
- **band_low_hz / band_high_hz** (default 300–3400 Hz) — frequency band
  for the band energy ratio feature.
- **weights** (default 0.2 each) — per-feature weights.  Weight energy
  heavily for clean environments, or spectral entropy for noisy ones.
