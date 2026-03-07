"""Tests for audio effects: delay/echo, tremolo, comb reverb."""

import numpy as np
import pytest

import pyminidsp as md


class TestDelayEcho:
    def test_shape(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.delay_echo(sig, delay_samples=100)
        assert out.shape == sig.shape

    def test_zero_feedback(self):
        """With feedback=0 and wet=1 dry=1, output should contain original + one delayed copy."""
        n = 1000
        delay = 100
        sig = md.impulse(n, amplitude=1.0, position=0)
        out = md.delay_echo(sig, delay_samples=delay, feedback=0.0, dry=1.0, wet=1.0)
        # Should have spike at 0 (dry) and at delay (single wet copy)
        assert out[0] == pytest.approx(1.0)
        assert out[delay] == pytest.approx(1.0)
        # No further echoes
        assert out[2 * delay] == pytest.approx(0.0, abs=1e-10)


class TestTremolo:
    def test_shape(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.tremolo(sig, rate_hz=5.0, depth=0.5, sample_rate=44100.0)
        assert out.shape == sig.shape

    def test_zero_depth_is_identity(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.tremolo(sig, rate_hz=5.0, depth=0.0, sample_rate=44100.0)
        np.testing.assert_allclose(out, sig, atol=1e-10)


class TestCombReverb:
    def test_shape(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.comb_reverb(sig, delay_samples=100)
        assert out.shape == sig.shape

    def test_energy_increases_with_feedback(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out_low = md.comb_reverb(sig, delay_samples=100, feedback=0.1, wet=0.5)
        out_high = md.comb_reverb(sig, delay_samples=100, feedback=0.8, wet=0.5)
        assert md.energy(out_high) > md.energy(out_low)
