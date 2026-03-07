"""Shared pytest fixtures for pyminidsp tests."""

import numpy as np
import pytest

import pyminidsp as md


@pytest.fixture
def sine_1k():
    """1024-sample sine wave at 1000 Hz, 44100 SR, amplitude 1.0."""
    return md.sine_wave(1024, amplitude=1.0, freq=1000.0, sample_rate=44100.0)


@pytest.fixture
def white_noise_1k():
    """1024-sample white noise with seed=42."""
    return md.white_noise(1024, seed=42)


@pytest.fixture
def impulse_100():
    """100-sample impulse at position 0, amplitude 1.0."""
    return md.impulse(100, amplitude=1.0, position=0)


@pytest.fixture
def dc_signal():
    """100-sample DC signal with value 1.0."""
    return np.ones(100, dtype=np.float64)


@pytest.fixture
def sample_rate():
    """Standard sample rate."""
    return 44100.0
