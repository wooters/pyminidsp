"""Tests for signal generators."""

import math

import numpy as np
import pytest

import pyminidsp as md


class TestSineWave:
    def test_shape_and_dtype(self):
        sig = md.sine_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert sig.shape == (1024,)
        assert sig.dtype == np.float64

    def test_amplitude_bounds(self):
        sig = md.sine_wave(4096, amplitude=0.5, freq=100.0, sample_rate=44100.0)
        assert sig.max() <= 0.5 + 1e-10
        assert sig.min() >= -0.5 - 1e-10

    def test_rms(self):
        sig = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert abs(md.rms(sig) - 1.0 / math.sqrt(2)) < 0.01

    def test_frequency_content(self):
        sr = 44100.0
        freq = 1000.0
        n = 4096
        sig = md.sine_wave(n, amplitude=1.0, freq=freq, sample_rate=sr)
        mag = md.magnitude_spectrum(sig)
        peak_bin = np.argmax(mag)
        expected_bin = round(freq * n / sr)
        assert abs(peak_bin - expected_bin) <= 1

    def test_zero_amplitude(self):
        sig = md.sine_wave(100, amplitude=0.0, freq=440.0, sample_rate=44100.0)
        np.testing.assert_allclose(sig, 0.0, atol=1e-15)


class TestWhiteNoise:
    def test_reproducible(self):
        n1 = md.white_noise(1024, seed=42)
        n2 = md.white_noise(1024, seed=42)
        np.testing.assert_array_equal(n1, n2)

    def test_different_seeds(self):
        n1 = md.white_noise(1024, seed=42)
        n2 = md.white_noise(1024, seed=99)
        assert not np.allclose(n1, n2)

    def test_statistical_properties(self):
        noise = md.white_noise(100000, amplitude=1.0, seed=7)
        assert abs(np.mean(noise)) < 0.05
        assert abs(np.std(noise) - 1.0) < 0.05

    def test_amplitude_scaling(self):
        noise = md.white_noise(100000, amplitude=0.5, seed=7)
        assert abs(np.std(noise) - 0.5) < 0.05


class TestImpulse:
    def test_basic(self):
        sig = md.impulse(100, amplitude=2.0, position=10)
        assert sig[10] == 2.0
        assert sig[0] == 0.0
        assert sig[99] == 0.0
        assert np.sum(sig != 0) == 1

    def test_energy(self):
        amp = 3.0
        sig = md.impulse(100, amplitude=amp, position=5)
        assert md.energy(sig) == pytest.approx(amp**2)

    def test_position_zero(self):
        sig = md.impulse(50, amplitude=1.0, position=0)
        assert sig[0] == 1.0
        assert np.sum(sig != 0) == 1


class TestChirpLinear:
    def test_shape(self):
        sig = md.chirp_linear(16000, amplitude=1.0, f_start=200.0,
                              f_end=4000.0, sample_rate=16000.0)
        assert sig.shape == (16000,)

    def test_amplitude_bounds(self):
        sig = md.chirp_linear(16000, amplitude=1.0, f_start=200.0,
                              f_end=4000.0, sample_rate=16000.0)
        assert sig.max() <= 1.0 + 1e-10

    def test_frequency_sweep(self):
        """Start and end halves should have different spectral content."""
        sr = 16000.0
        n = 16000
        sig = md.chirp_linear(n, amplitude=1.0, f_start=200.0,
                              f_end=4000.0, sample_rate=sr)
        mag_first = md.magnitude_spectrum(sig[:n // 2])
        mag_second = md.magnitude_spectrum(sig[n // 2:])
        peak_first = np.argmax(mag_first)
        peak_second = np.argmax(mag_second)
        assert peak_second > peak_first


class TestChirpLog:
    def test_shape(self):
        sig = md.chirp_log(44100, amplitude=1.0, f_start=20.0,
                           f_end=20000.0, sample_rate=44100.0)
        assert sig.shape == (44100,)


class TestSquareWave:
    def test_shape(self):
        sig = md.square_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert sig.shape == (1024,)

    def test_values(self):
        sig = md.square_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        unique_abs = np.unique(np.abs(sig))
        assert len(unique_abs) <= 2

    def test_rms_equals_amplitude(self):
        amp = 0.8
        sig = md.square_wave(44100, amplitude=amp, freq=100.0, sample_rate=44100.0)
        assert md.rms(sig) == pytest.approx(amp, abs=0.05)


class TestSawtoothWave:
    def test_shape(self):
        sig = md.sawtooth_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert sig.shape == (1024,)

    def test_range_bounds(self):
        amp = 1.0
        sig = md.sawtooth_wave(44100, amplitude=amp, freq=100.0, sample_rate=44100.0)
        assert sig.max() <= amp + 1e-10
        assert sig.min() >= -amp - 1e-10


class TestShepardTone:
    def test_shape(self):
        sig = md.shepard_tone(44100, amplitude=0.8, base_freq=440.0,
                              sample_rate=44100.0)
        assert sig.shape == (44100,)

    def test_dtype(self):
        sig = md.shepard_tone(1000, amplitude=0.5, base_freq=440.0,
                              sample_rate=44100.0)
        assert sig.dtype == np.float64


class TestSpectrogramText:
    def test_basic(self):
        sig = md.spectrogram_text("HI", freq_lo=200.0, freq_hi=7500.0,
                                  duration_sec=1.0, sample_rate=16000.0)
        assert len(sig) > 0
        assert sig.dtype == np.float64
