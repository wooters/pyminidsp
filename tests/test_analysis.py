"""Tests for signal measurement, analysis, and scaling functions."""

import math

import numpy as np
import pytest

import pyminidsp as md


class TestDotProduct:
    def test_basic(self):
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([4.0, 5.0, 6.0])
        assert md.dot(a, b) == pytest.approx(32.0)

    def test_commutativity(self):
        a = np.array([1.0, 3.0, -2.0])
        b = np.array([4.0, -1.0, 5.0])
        assert md.dot(a, b) == pytest.approx(md.dot(b, a))

    def test_orthogonal_vectors(self):
        a = np.array([1.0, 0.0])
        b = np.array([0.0, 1.0])
        assert md.dot(a, b) == pytest.approx(0.0)

    def test_self_dot_equals_energy(self):
        a = np.array([2.0, 3.0, 4.0])
        assert md.dot(a, a) == pytest.approx(md.energy(a))


class TestEnergy:
    def test_ones(self):
        sig = np.ones(100)
        assert md.energy(sig) == pytest.approx(100.0)

    def test_known_values(self):
        sig = np.array([3.0, 4.0])
        assert md.energy(sig) == pytest.approx(25.0)

    def test_zeros(self):
        sig = np.zeros(50)
        assert md.energy(sig) == pytest.approx(0.0)


class TestPower:
    def test_ones(self):
        sig = np.ones(100)
        assert md.power(sig) == pytest.approx(1.0)

    def test_relationship_to_energy(self):
        sig = np.array([1.0, 2.0, 3.0, 4.0])
        assert md.power(sig) == pytest.approx(md.energy(sig) / len(sig))


class TestPowerDb:
    def test_unit_signal(self):
        sig = np.ones(100)
        assert md.power_db(sig) == pytest.approx(0.0, abs=1e-10)

    def test_known_attenuation(self):
        sig = np.ones(100) * 0.1
        db = md.power_db(sig)
        assert db < 0.0  # power < 1 => negative dB


class TestRMS:
    def test_dc(self):
        sig = np.full(100, 3.0)
        assert md.rms(sig) == pytest.approx(3.0, abs=1e-10)

    def test_sine_rms(self):
        sig = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert md.rms(sig) == pytest.approx(1.0 / math.sqrt(2), abs=0.01)


class TestEntropy:
    def test_uniform_higher_than_sparse(self):
        uniform = np.ones(100) / 100.0
        sparse = np.zeros(100)
        sparse[0] = 1.0
        assert md.entropy(uniform) > md.entropy(sparse)


class TestZeroCrossingRate:
    def test_sine(self):
        sig = md.sine_wave(16000, freq=1000.0, sample_rate=16000.0)
        zcr = md.zero_crossing_rate(sig)
        assert abs(zcr - 0.125) < 0.01

    def test_dc_is_zero(self, dc_signal):
        zcr = md.zero_crossing_rate(dc_signal)
        assert zcr == pytest.approx(0.0, abs=1e-10)


class TestAutocorrelation:
    def test_lag_zero_is_one(self, sine_1k):
        acf = md.autocorrelation(sine_1k, 50)
        assert acf[0] == pytest.approx(1.0)
        assert len(acf) == 50

    def test_white_noise_decorrelates(self, white_noise_1k):
        acf = md.autocorrelation(white_noise_1k, 50)
        assert acf[0] == pytest.approx(1.0)
        # Non-zero lags should be small for white noise
        assert np.max(np.abs(acf[5:])) < 0.2


class TestPeakDetect:
    def test_basic(self):
        sig = np.array([0.0, 1.0, 3.0, 1.0, 0.0, 2.0, 5.0, 2.0, 0.0])
        peaks = md.peak_detect(sig, threshold=0.0, min_distance=1)
        assert list(peaks) == [2, 6]

    def test_no_peaks(self):
        sig = np.zeros(10)
        peaks = md.peak_detect(sig, threshold=1.0, min_distance=1)
        assert len(peaks) == 0


class TestF0:
    def test_autocorrelation(self):
        sig = md.sine_wave(4096, freq=200.0, sample_rate=16000.0)
        f0 = md.f0_autocorrelation(sig, 16000.0, 80.0, 400.0)
        assert abs(f0 - 200.0) < 5.0

    def test_fft(self):
        sig = md.sine_wave(4096, freq=200.0, sample_rate=16000.0)
        f0 = md.f0_fft(sig, 16000.0, 80.0, 400.0)
        assert abs(f0 - 200.0) < 10.0


class TestMix:
    def test_equal_mix(self):
        a = np.ones(100)
        b = np.ones(100) * 2.0
        out = md.mix(a, b, w_a=0.5, w_b=0.5)
        np.testing.assert_allclose(out, 1.5)

    def test_identity_a(self):
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([10.0, 20.0, 30.0])
        out = md.mix(a, b, w_a=1.0, w_b=0.0)
        np.testing.assert_allclose(out, a)

    def test_identity_b(self):
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([10.0, 20.0, 30.0])
        out = md.mix(a, b, w_a=0.0, w_b=1.0)
        np.testing.assert_allclose(out, b)


class TestScale:
    def test_midpoint(self):
        assert md.scale(5.0, 0.0, 10.0, 0.0, 100.0) == pytest.approx(50.0)

    def test_endpoints(self):
        assert md.scale(0.0, 0.0, 10.0, 0.0, 100.0) == pytest.approx(0.0)
        assert md.scale(10.0, 0.0, 10.0, 0.0, 100.0) == pytest.approx(100.0)


class TestScaleVec:
    def test_basic(self):
        a = np.array([0.0, 5.0, 10.0])
        out = md.scale_vec(a, 0.0, 10.0, 0.0, 100.0)
        np.testing.assert_allclose(out, [0.0, 50.0, 100.0])


class TestFitWithinRange:
    def test_basic(self):
        a = np.array([-2.0, 0.0, 2.0])
        out = md.fit_within_range(a, 0.0, 1.0)
        assert out.min() >= 0.0
        assert out.max() <= 1.0

    def test_already_in_range(self):
        a = np.array([0.2, 0.5, 0.8])
        out = md.fit_within_range(a, 0.0, 1.0)
        assert out.min() >= 0.0
        assert out.max() <= 1.0


class TestAdjustDblevel:
    def test_shape_preserved(self):
        sig = md.sine_wave(4096, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        out = md.adjust_dblevel(sig, -20.0)
        assert out.shape == sig.shape

    def test_attenuates(self):
        sig = md.sine_wave(4096, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        out = md.adjust_dblevel(sig, -20.0)
        assert md.rms(out) < md.rms(sig)
