"""Tests for voice activity detection (VAD)."""

import numpy as np
import pytest

import pyminidsp as md


class TestVADConstruction:
    def test_default(self):
        v = md.VAD()
        assert v is not None

    def test_custom_threshold(self):
        v = md.VAD(threshold=0.3)
        assert v is not None

    def test_custom_hangover(self):
        v = md.VAD(hangover_frames=20, onset_frames=5)
        assert v is not None

    def test_custom_weights(self):
        v = md.VAD(weights=[0.4, 0.1, 0.1, 0.1, 0.3])
        assert v is not None

    def test_custom_band(self):
        v = md.VAD(band_low_hz=200.0, band_high_hz=4000.0)
        assert v is not None

    def test_wrong_weights_length(self):
        with pytest.raises(ValueError, match="5 elements"):
            md.VAD(weights=[0.5, 0.5])


class TestCalibrate:
    def test_calibrate_silence(self):
        v = md.VAD()
        silence = np.zeros(320, dtype=np.float64)
        # Should not raise
        v.calibrate(silence, sample_rate=16000.0)

    def test_calibrate_multiple(self):
        v = md.VAD()
        silence = np.zeros(320, dtype=np.float64)
        for _ in range(10):
            v.calibrate(silence, sample_rate=16000.0)


class TestProcessFrame:
    def test_silence_returns_zero(self):
        v = md.VAD()
        silence = np.zeros(320, dtype=np.float64)
        # Calibrate first
        for _ in range(5):
            v.calibrate(silence, sample_rate=16000.0)
        decision, score, features = v.process_frame(silence, 16000.0)
        assert decision == 0

    def test_loud_tone_returns_one(self):
        v = md.VAD()
        sr = 16000.0
        frame_len = 320
        silence = np.zeros(frame_len, dtype=np.float64)
        # Calibrate with silence
        for _ in range(10):
            v.calibrate(silence, sample_rate=sr)
        # Generate a loud sine tone that should trigger detection
        tone = md.sine_wave(frame_len, amplitude=1.0, freq=1000.0, sample_rate=sr)
        # Process several frames to get past onset
        for _ in range(10):
            decision, score, features = v.process_frame(tone, sr)
        assert decision == 1

    def test_return_types(self):
        v = md.VAD()
        frame = np.zeros(320, dtype=np.float64)
        decision, score, features = v.process_frame(frame, 16000.0)
        assert isinstance(decision, int)
        assert isinstance(score, float)
        assert isinstance(features, np.ndarray)
        assert features.dtype == np.float64
        assert len(features) == md.VAD_NUM_FEATURES

    def test_score_in_range(self):
        v = md.VAD()
        frame = md.sine_wave(320, amplitude=0.5, freq=500.0, sample_rate=16000.0)
        _, score, _ = v.process_frame(frame, 16000.0)
        assert 0.0 <= score <= 1.0

    def test_noncontiguous_input(self):
        v = md.VAD()
        # Create a non-contiguous array via slicing
        big = np.zeros(640, dtype=np.float64)
        frame = big[::2]  # non-contiguous: every other element
        assert not frame.flags["C_CONTIGUOUS"]
        decision, score, features = v.process_frame(frame, 16000.0)
        assert isinstance(decision, int)


class TestProcess:
    def test_batch_shapes(self):
        v = md.VAD()
        sr = 16000.0
        frame_len = 320
        num_frames = 50
        signal = np.zeros(frame_len * num_frames, dtype=np.float64)
        decisions, scores, features = v.process(signal, sr, frame_len)
        assert decisions.shape == (num_frames,)
        assert decisions.dtype == np.int32
        assert scores.shape == (num_frames,)
        assert scores.dtype == np.float64
        assert features.shape == (num_frames, 5)
        assert features.dtype == np.float64

    def test_all_silence(self):
        v = md.VAD()
        sr = 16000.0
        frame_len = 320
        signal = np.zeros(frame_len * 20, dtype=np.float64)
        decisions, _, _ = v.process(signal, sr, frame_len)
        assert np.all(decisions == 0)

    def test_partial_frame_truncated(self):
        v = md.VAD()
        sr = 16000.0
        frame_len = 320
        # 3.5 frames worth of samples — should produce 3 frames
        signal = np.zeros(frame_len * 3 + 160, dtype=np.float64)
        decisions, scores, features = v.process(signal, sr, frame_len)
        assert len(decisions) == 3


class TestVADNumFeatures:
    def test_constant_value(self):
        assert md.VAD_NUM_FEATURES == 5

    def test_in_all(self):
        assert "VAD_NUM_FEATURES" in md.__all__
        assert "VAD" in md.__all__
