"""Voice activity detection (VAD) with adaptive normalization."""

from __future__ import annotations

from typing import Sequence

import numpy as np
import numpy.typing as npt

from pyminidsp._minidsp_cffi import ffi, lib
from pyminidsp._helpers import _as_double_ptr, _new_double_array, _check_error, VAD_NUM_FEATURES


class VAD:
    """
    Voice activity detector with adaptive feature normalization and
    onset/hangover smoothing.

    Wraps the miniDSP C library's stateful VAD API.  The detector extracts
    five features per frame (energy, ZCR, spectral entropy, spectral
    flatness, band energy ratio), normalizes them adaptively, computes a
    weighted score, and applies an onset/hangover state machine.

    Example:
        >>> detector = VAD(threshold=0.4)
        >>> detector.calibrate(silence_frame, sample_rate=16000.0)
        >>> decision, score, features = detector.process_frame(frame, 16000.0)
    """

    def __init__(
        self,
        *,
        threshold: float | None = None,
        onset_frames: int | None = None,
        hangover_frames: int | None = None,
        adaptation_rate: float | None = None,
        band_low_hz: float | None = None,
        band_high_hz: float | None = None,
        weights: Sequence[float] | None = None,
    ) -> None:
        """
        Create a new VAD detector.

        All parameters are optional.  Omitted parameters use the C library
        defaults (threshold=0.5, onset_frames=3, hangover_frames=15,
        adaptation_rate=0.01, band 300–3400 Hz, equal weights of 0.2).

        Args:
            threshold: Decision threshold in [0.0, 1.0].
            onset_frames: Consecutive above-threshold frames before speech.
            hangover_frames: Frames to remain in speech after activity drops.
            adaptation_rate: EMA learning rate for normalization.
            band_low_hz: Lower bound of speech band in Hz.
            band_high_hz: Upper bound of speech band in Hz.
            weights: Per-feature weights (length 5).
        """
        self._params = ffi.new("MD_vad_params *")
        lib.MD_vad_default_params(self._params)

        if threshold is not None:
            self._params.threshold = threshold
        if onset_frames is not None:
            self._params.onset_frames = onset_frames
        if hangover_frames is not None:
            self._params.hangover_frames = hangover_frames
        if adaptation_rate is not None:
            self._params.adaptation_rate = adaptation_rate
        if band_low_hz is not None:
            self._params.band_low_hz = band_low_hz
        if band_high_hz is not None:
            self._params.band_high_hz = band_high_hz
        if weights is not None:
            if len(weights) != VAD_NUM_FEATURES:
                raise ValueError(
                    f"weights must have {VAD_NUM_FEATURES} elements, "
                    f"got {len(weights)}"
                )
            for i, w in enumerate(weights):
                self._params.weights[i] = w

        self._state = ffi.new("MD_vad_state *")
        lib.MD_vad_init(self._state, self._params)
        _check_error()

    def calibrate(self, signal: npt.ArrayLike, sample_rate: float) -> None:
        """
        Feed a known-silence frame to seed the adaptive normalization.

        Call this on several silence frames before live processing to
        improve initial accuracy.

        Args:
            signal: Frame samples (1-D array).
            sample_rate: Sample rate in Hz.
        """
        s_ptr, signal = _as_double_ptr(signal)
        lib.MD_vad_calibrate(self._state, s_ptr, len(signal), float(sample_rate))
        _check_error()

    def process_frame(
        self, signal: npt.ArrayLike, sample_rate: float
    ) -> tuple[int, float, npt.NDArray[np.float64]]:
        """
        Process one audio frame and return the VAD decision.

        Args:
            signal: Frame samples (1-D array).
            sample_rate: Sample rate in Hz.

        Returns:
            A tuple of ``(decision, score, features)`` where *decision* is
            1 (speech) or 0 (silence), *score* is the combined weighted
            score in [0.0, 1.0], and *features* is a float64 array of
            length 5 containing the normalized feature values.
        """
        s_ptr, signal = _as_double_ptr(signal)
        score_out = ffi.new("double *")
        features, feat_ptr = _new_double_array(VAD_NUM_FEATURES)
        decision = lib.MD_vad_process_frame(
            self._state, s_ptr, len(signal), float(sample_rate),
            score_out, feat_ptr,
        )
        _check_error()
        return int(decision), float(score_out[0]), features

    def process(
        self,
        signal: npt.ArrayLike,
        sample_rate: float,
        frame_len: int,
    ) -> tuple[npt.NDArray[np.int32], npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """
        Segment a signal into non-overlapping frames and process each one.

        Args:
            signal: Input signal (1-D array).
            sample_rate: Sample rate in Hz.
            frame_len: Number of samples per frame.

        Returns:
            A tuple of ``(decisions, scores, features)`` where *decisions*
            is an int32 array of length *num_frames*, *scores* is a float64
            array of length *num_frames*, and *features* is a float64 array
            of shape ``(num_frames, 5)``.
        """
        signal = np.ascontiguousarray(signal, dtype=np.float64)
        num_frames = len(signal) // frame_len
        decisions = np.empty(num_frames, dtype=np.int32)
        scores = np.empty(num_frames, dtype=np.float64)
        all_features = np.empty((num_frames, VAD_NUM_FEATURES), dtype=np.float64)

        for i in range(num_frames):
            frame = signal[i * frame_len : (i + 1) * frame_len]
            d, s, f = self.process_frame(frame, sample_rate)
            decisions[i] = d
            scores[i] = s
            all_features[i] = f

        return decisions, scores, all_features
