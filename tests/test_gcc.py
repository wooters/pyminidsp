"""Tests for Generalized Cross-Correlation (GCC) delay estimation."""

import numpy as np
import pytest

import pyminidsp as md


class TestGetDelay:
    def test_positive_delay(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        sig_b = np.roll(sig_a, 5)
        delay, ent = md.get_delay(sig_a, sig_b, margin=20, weighting=md.GCC_PHAT)
        assert delay == 5

    def test_negative_delay(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        sig_b = np.roll(sig_a, -5)
        delay, ent = md.get_delay(sig_a, sig_b, margin=20, weighting=md.GCC_PHAT)
        assert delay == -5

    def test_zero_delay(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        delay, ent = md.get_delay(sig, sig, margin=20, weighting=md.GCC_PHAT)
        assert delay == 0

    def test_gcc_simp_weighting(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        sig_b = np.roll(sig_a, 3)
        delay, ent = md.get_delay(sig_a, sig_b, margin=20, weighting=md.GCC_SIMP)
        assert abs(delay - 3) <= 1


class TestGcc:
    def test_shape(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        sig_b = np.roll(sig_a, 3)
        corr = md.gcc(sig_a, sig_b, weighting=md.GCC_PHAT)
        assert corr.shape == (1024,)

    def test_dtype(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        corr = md.gcc(sig_a, sig_a, weighting=md.GCC_PHAT)
        assert corr.dtype == np.float64


class TestGetMultipleDelays:
    def test_basic(self):
        ref = md.sine_wave(2048, freq=440.0, sample_rate=44100.0)
        sig1 = np.roll(ref, 3)
        sig2 = np.roll(ref, 7)
        delays = md.get_multiple_delays([ref, sig1, sig2], margin=20)
        assert delays.shape == (2,)
        assert abs(delays[0] - 3) <= 1
        assert abs(delays[1] - 7) <= 1


class TestGccConstants:
    def test_values(self):
        assert md.GCC_SIMP == 0
        assert md.GCC_PHAT == 1
