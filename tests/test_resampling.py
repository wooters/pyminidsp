"""Tests for polyphase sinc resampling."""

import numpy as np
import pytest

import pyminidsp as md


class TestResampleOutputLen:
    def test_upsample_2x(self):
        assert md.resample_output_len(1000, 22050.0, 44100.0) == 2000

    def test_downsample_2x(self):
        assert md.resample_output_len(1000, 44100.0, 22050.0) == 500

    def test_same_rate(self):
        assert md.resample_output_len(1000, 44100.0, 44100.0) == 1000


class TestResample:
    def test_upsample_length(self):
        sig = md.sine_wave(1000, freq=440.0, sample_rate=22050.0)
        out = md.resample(sig, in_rate=22050.0, out_rate=44100.0)
        assert len(out) == 2000

    def test_downsample_length(self):
        sig = md.sine_wave(1000, freq=440.0, sample_rate=44100.0)
        out = md.resample(sig, in_rate=44100.0, out_rate=22050.0)
        assert len(out) == 500

    def test_preserves_tone_below_nyquist(self):
        sr_in = 44100.0
        sr_out = 22050.0
        freq = 1000.0  # well below new Nyquist (11025 Hz)
        sig = md.sine_wave(8192, freq=freq, sample_rate=sr_in)
        out = md.resample(sig, in_rate=sr_in, out_rate=sr_out)
        # Estimate F0 of resampled signal
        f0 = md.f0_fft(out, sr_out, 500.0, 1500.0)
        assert abs(f0 - freq) < 50.0

    def test_output_dtype(self):
        sig = md.sine_wave(1000, freq=440.0, sample_rate=44100.0)
        out = md.resample(sig, in_rate=44100.0, out_rate=48000.0)
        assert out.dtype == np.float64
