"""Tests for FIR filters, convolution, and biquad (IIR) filtering."""

import numpy as np
import pytest

import pyminidsp as md


class TestConvolutionNumSamples:
    def test_basic(self):
        assert md.convolution_num_samples(100, 10) == 109


class TestConvolutionTime:
    def test_impulse_response(self, impulse_100):
        kernel = np.array([1.0, 2.0, 3.0])
        out = md.convolution_time(impulse_100, kernel)
        assert len(out) == 102
        np.testing.assert_allclose(out[:3], [1.0, 2.0, 3.0])

    def test_impulse_is_identity(self):
        sig = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        unit_impulse = np.array([1.0])
        out = md.convolution_time(sig, unit_impulse)
        np.testing.assert_allclose(out, sig)

    def test_commutativity(self):
        a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        b = np.array([0.5, 1.0, 0.5])
        out_ab = md.convolution_time(a, b)
        out_ba = md.convolution_time(b, a)
        np.testing.assert_allclose(out_ab, out_ba, atol=1e-10)


class TestMovingAverage:
    def test_constant_signal(self, dc_signal):
        out = md.moving_average(dc_signal, window_len=5)
        assert out.shape == (100,)
        np.testing.assert_allclose(out[4:], 1.0)

    def test_shape_preserved(self):
        sig = md.sine_wave(200, freq=100.0, sample_rate=8000.0)
        out = md.moving_average(sig, window_len=10)
        assert out.shape == sig.shape


class TestFirFilter:
    def test_impulse_response(self, impulse_100):
        coeffs = np.array([0.25, 0.5, 0.25])
        out = md.fir_filter(impulse_100, coeffs)
        assert out.shape == (100,)
        np.testing.assert_allclose(out[:3], [0.25, 0.5, 0.25])

    def test_all_pass(self):
        sig = md.sine_wave(200, freq=100.0, sample_rate=8000.0)
        coeffs = np.array([1.0])
        out = md.fir_filter(sig, coeffs)
        np.testing.assert_allclose(out, sig)


class TestConvolutionFftOla:
    def test_impulse_response(self, impulse_100):
        kernel = np.array([1.0, 2.0, 3.0])
        out = md.convolution_fft_ola(impulse_100, kernel)
        assert len(out) == 102
        np.testing.assert_allclose(out[:3], [1.0, 2.0, 3.0], atol=1e-10)

    def test_matches_time_domain(self):
        sig = md.sine_wave(256, freq=440.0, sample_rate=8000.0)
        kernel = np.array([0.2, 0.3, 0.5, 0.3, 0.2])
        out_time = md.convolution_time(sig, kernel)
        out_fft = md.convolution_fft_ola(sig, kernel)
        np.testing.assert_allclose(out_fft, out_time, atol=1e-8)


class TestBiquadFilter:
    def test_create(self):
        filt = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
        assert filt is not None

    def test_process_single(self):
        filt = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
        result = filt.process(1.0)
        assert isinstance(result, float)

    def test_process_array_shape(self, sine_1k):
        filt = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
        out = filt.process_array(sine_1k)
        assert out.shape == sine_1k.shape

    def test_lowpass_attenuates_high_freq(self):
        filt = md.BiquadFilter(md.LPF, freq=500.0, sample_rate=44100.0)
        high = md.sine_wave(4096, freq=5000.0, sample_rate=44100.0)
        out = filt.process_array(high)
        assert md.rms(out) < md.rms(high) * 0.5

    def test_highpass_passes_high_freq(self):
        filt = md.BiquadFilter(md.HPF, freq=500.0, sample_rate=44100.0)
        high = md.sine_wave(4096, freq=5000.0, sample_rate=44100.0)
        out = filt.process_array(high)
        # HPF should pass high frequencies with minimal attenuation
        assert md.rms(out) > md.rms(high) * 0.5

    def test_bandpass_passes_center(self):
        center = 1000.0
        filt = md.BiquadFilter(md.BPF, freq=center, sample_rate=44100.0)
        sig = md.sine_wave(4096, freq=center, sample_rate=44100.0)
        out = filt.process_array(sig)
        assert md.rms(out) > 0.1

    def test_all_filter_types(self):
        for ftype in [md.LPF, md.HPF, md.BPF, md.NOTCH, md.PEQ, md.LSH, md.HSH]:
            filt = md.BiquadFilter(ftype, freq=1000.0, sample_rate=44100.0,
                                   db_gain=6.0)
            assert filt is not None


class TestConstants:
    def test_filter_type_constants(self):
        assert md.LPF == 0
        assert md.HPF == 1
        assert md.BPF == 2
        assert md.NOTCH == 3
        assert md.PEQ == 4
        assert md.LSH == 5
        assert md.HSH == 6
