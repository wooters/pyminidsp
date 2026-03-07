"""Tests for FFT spectrum, STFT, mel filterbanks, MFCCs, and windows."""

import math

import numpy as np
import pytest

import pyminidsp as md


class TestMagnitudeSpectrum:
    def test_shape(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        mag = md.magnitude_spectrum(sig)
        assert mag.shape == (513,)
        assert mag.max() > 0

    def test_peak_at_correct_bin(self):
        sr = 16000.0
        freq = 1000.0
        n = 1024
        sig = md.sine_wave(n, freq=freq, sample_rate=sr)
        mag = md.magnitude_spectrum(sig)
        peak_bin = np.argmax(mag)
        expected_bin = round(freq * n / sr)
        assert abs(peak_bin - expected_bin) <= 1

    def test_dc_signal(self):
        sig = np.ones(256)
        mag = md.magnitude_spectrum(sig)
        # DC component (bin 0) should dominate
        assert np.argmax(mag) == 0


class TestPowerSpectralDensity:
    def test_shape(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        psd = md.power_spectral_density(sig)
        assert psd.shape == (513,)

    def test_parseval_theorem(self):
        """Time-domain energy should approximately equal frequency-domain energy."""
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        time_energy = md.energy(sig)
        psd = md.power_spectral_density(sig)
        # One-sided PSD: DC and Nyquist counted once, others doubled
        freq_energy = psd[0] + 2 * np.sum(psd[1:-1]) + psd[-1]
        assert freq_energy == pytest.approx(time_energy, rel=0.01)


class TestPhaseSpectrum:
    def test_shape_and_bounds(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        phase = md.phase_spectrum(sig)
        assert phase.shape == (513,)
        assert phase.max() <= math.pi + 1e-10
        assert phase.min() >= -math.pi - 1e-10

    def test_cosine_phase_near_zero(self):
        """A cosine wave should have phase ~0 at its peak frequency bin."""
        sr = 16000.0
        n = 1024
        freq = 500.0
        # cos(2*pi*f*t) = Re(e^{j*2*pi*f*t}), phase should be ~0
        t = np.arange(n) / sr
        sig = np.cos(2 * math.pi * freq * t)
        phase = md.phase_spectrum(sig)
        mag = md.magnitude_spectrum(sig)
        peak_bin = np.argmax(mag)
        assert abs(phase[peak_bin]) < 0.2


class TestSTFT:
    def test_shape(self):
        sig = md.sine_wave(16000, freq=440.0, sample_rate=16000.0)
        spec = md.stft(sig, n=512, hop=128)
        expected_frames = md.stft_num_frames(16000, 512, 128)
        assert spec.shape == (expected_frames, 257)

    def test_frame_count_consistency(self):
        for sig_len in [1024, 2048, 4000]:
            for n, hop in [(256, 64), (512, 128), (512, 256)]:
                expected = md.stft_num_frames(sig_len, n, hop)
                sig = md.sine_wave(sig_len, freq=440.0, sample_rate=16000.0)
                spec = md.stft(sig, n=n, hop=hop)
                assert spec.shape[0] == expected


class TestMelFilterbank:
    def test_shape(self):
        fb = md.mel_filterbank(512, sample_rate=16000.0, num_mels=26)
        assert fb.shape == (26, 257)
        assert fb.min() >= 0.0

    def test_column_sums_bounded(self):
        fb = md.mel_filterbank(512, sample_rate=16000.0, num_mels=26)
        col_sums = fb.sum(axis=0)
        assert col_sums.max() <= 1.0 + 1e-10


class TestMelEnergies:
    def test_shape(self):
        sig = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
        mel = md.mel_energies(sig, sample_rate=16000.0, num_mels=26)
        assert mel.shape == (26,)

    def test_non_negative(self):
        sig = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
        mel = md.mel_energies(sig, sample_rate=16000.0, num_mels=26)
        assert mel.min() >= 0.0


class TestMFCC:
    def test_shape(self):
        sig = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
        coeffs = md.mfcc(sig, sample_rate=16000.0, num_mels=26, num_coeffs=13)
        assert coeffs.shape == (13,)

    def test_different_num_coeffs(self):
        sig = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
        for nc in [5, 13, 20]:
            coeffs = md.mfcc(sig, sample_rate=16000.0, num_mels=26, num_coeffs=nc)
            assert coeffs.shape == (nc,)


class TestHannWindow:
    def test_shape_and_endpoints(self):
        win = md.hann_window(256)
        assert win.shape == (256,)
        assert win[0] == pytest.approx(0.0, abs=1e-10)
        assert win[-1] == pytest.approx(0.0, abs=1e-10)

    def test_peak(self):
        win = md.hann_window(256)
        assert win[128] == pytest.approx(1.0, abs=1e-3)

    def test_symmetry(self):
        win = md.hann_window(256)
        np.testing.assert_allclose(win, win[::-1], atol=1e-10)


class TestHammingWindow:
    def test_shape_and_peak(self):
        win = md.hamming_window(256)
        assert win.shape == (256,)
        assert win[128] == pytest.approx(1.0, abs=1e-2)

    def test_symmetry(self):
        win = md.hamming_window(256)
        np.testing.assert_allclose(win, win[::-1], atol=1e-10)


class TestBlackmanWindow:
    def test_shape(self):
        win = md.blackman_window(256)
        assert win.shape == (256,)

    def test_symmetry(self):
        win = md.blackman_window(256)
        np.testing.assert_allclose(win, win[::-1], atol=1e-10)


class TestRectWindow:
    def test_all_ones(self):
        win = md.rect_window(256)
        np.testing.assert_allclose(win, 1.0)

    def test_symmetry(self):
        win = md.rect_window(256)
        np.testing.assert_allclose(win, win[::-1])
