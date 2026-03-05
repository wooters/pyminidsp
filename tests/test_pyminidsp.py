"""Tests for the pyminidsp Python bindings."""

import math

import numpy as np
import pytest

import pyminidsp as md


# ---------------------------------------------------------------------------
# Signal generators
# ---------------------------------------------------------------------------

class TestGenerators:
    def test_sine_wave_shape(self):
        sig = md.sine_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert sig.shape == (1024,)
        assert sig.dtype == np.float64

    def test_sine_wave_amplitude(self):
        sig = md.sine_wave(4096, amplitude=0.5, freq=100.0, sample_rate=44100.0)
        assert sig.max() <= 0.5 + 1e-10
        assert sig.min() >= -0.5 - 1e-10

    def test_sine_wave_rms(self):
        sig = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert abs(md.rms(sig) - 1.0 / math.sqrt(2)) < 0.01

    def test_white_noise_reproducible(self):
        n1 = md.white_noise(1024, seed=42)
        n2 = md.white_noise(1024, seed=42)
        np.testing.assert_array_equal(n1, n2)

    def test_white_noise_different_seeds(self):
        n1 = md.white_noise(1024, seed=42)
        n2 = md.white_noise(1024, seed=99)
        assert not np.allclose(n1, n2)

    def test_impulse(self):
        sig = md.impulse(100, amplitude=2.0, position=10)
        assert sig[10] == 2.0
        assert sig[0] == 0.0
        assert sig[99] == 0.0
        assert np.sum(sig != 0) == 1

    def test_chirp_linear(self):
        sig = md.chirp_linear(16000, amplitude=1.0, f_start=200.0,
                              f_end=4000.0, sample_rate=16000.0)
        assert sig.shape == (16000,)
        assert sig.max() <= 1.0 + 1e-10

    def test_chirp_log(self):
        sig = md.chirp_log(44100, amplitude=1.0, f_start=20.0,
                           f_end=20000.0, sample_rate=44100.0)
        assert sig.shape == (44100,)

    def test_square_wave(self):
        sig = md.square_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert sig.shape == (1024,)
        # Square wave should only contain values near +1, -1, or 0
        unique_abs = np.unique(np.abs(sig))
        assert len(unique_abs) <= 2

    def test_sawtooth_wave(self):
        sig = md.sawtooth_wave(1024, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        assert sig.shape == (1024,)

    def test_shepard_tone(self):
        sig = md.shepard_tone(44100, amplitude=0.8, base_freq=440.0,
                              sample_rate=44100.0)
        assert sig.shape == (44100,)


# ---------------------------------------------------------------------------
# Signal measurement
# ---------------------------------------------------------------------------

class TestMeasurement:
    def test_dot_product(self):
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([4.0, 5.0, 6.0])
        assert md.dot(a, b) == pytest.approx(32.0)

    def test_energy(self):
        sig = np.ones(100)
        assert md.energy(sig) == pytest.approx(100.0)

    def test_power(self):
        sig = np.ones(100)
        assert md.power(sig) == pytest.approx(1.0)

    def test_power_db(self):
        sig = np.ones(100)
        assert md.power_db(sig) == pytest.approx(0.0, abs=1e-10)

    def test_rms_dc(self):
        sig = np.full(100, 3.0)
        assert md.rms(sig) == pytest.approx(3.0, abs=1e-10)


# ---------------------------------------------------------------------------
# Signal analysis
# ---------------------------------------------------------------------------

class TestAnalysis:
    def test_zero_crossing_rate(self):
        sig = md.sine_wave(16000, freq=1000.0, sample_rate=16000.0)
        zcr = md.zero_crossing_rate(sig)
        # ZCR ~ 2 * freq / sample_rate
        assert abs(zcr - 0.125) < 0.01

    def test_autocorrelation(self):
        sig = md.sine_wave(1024, freq=100.0, sample_rate=1000.0)
        acf = md.autocorrelation(sig, 50)
        assert acf[0] == pytest.approx(1.0)
        assert len(acf) == 50

    def test_peak_detect(self):
        sig = np.array([0.0, 1.0, 3.0, 1.0, 0.0, 2.0, 5.0, 2.0, 0.0])
        peaks = md.peak_detect(sig, threshold=0.0, min_distance=1)
        assert list(peaks) == [2, 6]

    def test_f0_autocorrelation(self):
        sig = md.sine_wave(4096, freq=200.0, sample_rate=16000.0)
        f0 = md.f0_autocorrelation(sig, 16000.0, 80.0, 400.0)
        assert abs(f0 - 200.0) < 5.0

    def test_f0_fft(self):
        sig = md.sine_wave(4096, freq=200.0, sample_rate=16000.0)
        f0 = md.f0_fft(sig, 16000.0, 80.0, 400.0)
        assert abs(f0 - 200.0) < 10.0

    def test_mix(self):
        a = np.ones(100)
        b = np.ones(100) * 2.0
        out = md.mix(a, b, w_a=0.5, w_b=0.5)
        np.testing.assert_allclose(out, 1.5)


# ---------------------------------------------------------------------------
# Effects
# ---------------------------------------------------------------------------

class TestEffects:
    def test_delay_echo_shape(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.delay_echo(sig, delay_samples=100)
        assert out.shape == sig.shape

    def test_tremolo_shape(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.tremolo(sig, rate_hz=5.0, depth=0.5, sample_rate=44100.0)
        assert out.shape == sig.shape

    def test_comb_reverb_shape(self):
        sig = md.sine_wave(4096, freq=440.0, sample_rate=44100.0)
        out = md.comb_reverb(sig, delay_samples=100)
        assert out.shape == sig.shape


# ---------------------------------------------------------------------------
# FIR / Convolution
# ---------------------------------------------------------------------------

class TestFIR:
    def test_convolution_num_samples(self):
        assert md.convolution_num_samples(100, 10) == 109

    def test_convolution_time(self):
        sig = md.impulse(100, amplitude=1.0, position=0)
        kernel = np.array([1.0, 2.0, 3.0])
        out = md.convolution_time(sig, kernel)
        assert len(out) == 102
        np.testing.assert_allclose(out[:3], [1.0, 2.0, 3.0])

    def test_moving_average(self):
        sig = np.ones(100)
        out = md.moving_average(sig, window_len=5)
        assert out.shape == (100,)
        # After startup, all values should be 1.0
        np.testing.assert_allclose(out[4:], 1.0)

    def test_fir_filter(self):
        sig = md.impulse(100, amplitude=1.0, position=0)
        coeffs = np.array([0.25, 0.5, 0.25])
        out = md.fir_filter(sig, coeffs)
        assert out.shape == (100,)
        np.testing.assert_allclose(out[:3], [0.25, 0.5, 0.25])

    def test_convolution_fft_ola(self):
        sig = md.impulse(100, amplitude=1.0, position=0)
        kernel = np.array([1.0, 2.0, 3.0])
        out = md.convolution_fft_ola(sig, kernel)
        assert len(out) == 102
        np.testing.assert_allclose(out[:3], [1.0, 2.0, 3.0], atol=1e-10)


# ---------------------------------------------------------------------------
# Scaling
# ---------------------------------------------------------------------------

class TestScaling:
    def test_scale(self):
        assert md.scale(5.0, 0.0, 10.0, 0.0, 100.0) == pytest.approx(50.0)

    def test_scale_vec(self):
        a = np.array([0.0, 5.0, 10.0])
        out = md.scale_vec(a, 0.0, 10.0, 0.0, 100.0)
        np.testing.assert_allclose(out, [0.0, 50.0, 100.0])

    def test_fit_within_range(self):
        a = np.array([-2.0, 0.0, 2.0])
        out = md.fit_within_range(a, 0.0, 1.0)
        assert out.min() >= 0.0
        assert out.max() <= 1.0

    def test_adjust_dblevel(self):
        sig = md.sine_wave(4096, amplitude=1.0, freq=440.0, sample_rate=44100.0)
        out = md.adjust_dblevel(sig, -20.0)
        assert out.shape == sig.shape


# ---------------------------------------------------------------------------
# Spectrum analysis
# ---------------------------------------------------------------------------

class TestSpectrum:
    def test_magnitude_spectrum(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        mag = md.magnitude_spectrum(sig)
        assert mag.shape == (513,)
        assert mag.max() > 0

    def test_power_spectral_density(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        psd = md.power_spectral_density(sig)
        assert psd.shape == (513,)

    def test_phase_spectrum(self):
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        phase = md.phase_spectrum(sig)
        assert phase.shape == (513,)
        assert phase.max() <= math.pi + 1e-10
        assert phase.min() >= -math.pi - 1e-10

    def test_stft(self):
        sig = md.sine_wave(16000, freq=440.0, sample_rate=16000.0)
        spec = md.stft(sig, n=512, hop=128)
        expected_frames = md.stft_num_frames(16000, 512, 128)
        assert spec.shape == (expected_frames, 257)

    def test_mel_filterbank(self):
        fb = md.mel_filterbank(512, sample_rate=16000.0, num_mels=26)
        assert fb.shape == (26, 257)
        assert fb.min() >= 0.0

    def test_mel_energies(self):
        sig = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
        mel = md.mel_energies(sig, sample_rate=16000.0, num_mels=26)
        assert mel.shape == (26,)

    def test_mfcc(self):
        sig = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
        coeffs = md.mfcc(sig, sample_rate=16000.0, num_mels=26, num_coeffs=13)
        assert coeffs.shape == (13,)


# ---------------------------------------------------------------------------
# Windows
# ---------------------------------------------------------------------------

class TestWindows:
    def test_hann_window(self):
        win = md.hann_window(256)
        assert win.shape == (256,)
        assert win[0] == pytest.approx(0.0, abs=1e-10)
        assert win[128] == pytest.approx(1.0, abs=1e-3)

    def test_hamming_window(self):
        win = md.hamming_window(256)
        assert win.shape == (256,)
        assert win[128] == pytest.approx(1.0, abs=1e-2)

    def test_blackman_window(self):
        win = md.blackman_window(256)
        assert win.shape == (256,)

    def test_rect_window(self):
        win = md.rect_window(256)
        np.testing.assert_allclose(win, 1.0)


# ---------------------------------------------------------------------------
# DTMF
# ---------------------------------------------------------------------------

class TestDTMF:
    def test_dtmf_signal_length(self):
        length = md.dtmf_signal_length(3, sample_rate=8000.0, tone_ms=70, pause_ms=70)
        assert length > 0

    def test_dtmf_roundtrip(self):
        digits = "5551234"
        sig = md.dtmf_generate(digits, sample_rate=8000.0)
        detected = md.dtmf_detect(sig, sample_rate=8000.0)
        detected_digits = "".join(t[0] for t in detected)
        assert detected_digits == digits

    def test_dtmf_timing(self):
        sig = md.dtmf_generate("1", sample_rate=8000.0, tone_ms=70, pause_ms=70)
        tones = md.dtmf_detect(sig, sample_rate=8000.0)
        assert len(tones) == 1
        assert tones[0][0] == "1"
        assert tones[0][1] >= 0.0  # start_s


# ---------------------------------------------------------------------------
# GCC delay estimation
# ---------------------------------------------------------------------------

class TestGCC:
    def test_get_delay(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        sig_b = np.roll(sig_a, 5)
        delay, ent = md.get_delay(sig_a, sig_b, margin=20, weighting=md.GCC_PHAT)
        assert delay == 5

    def test_gcc_shape(self):
        sig_a = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        sig_b = np.roll(sig_a, 3)
        corr = md.gcc(sig_a, sig_b, weighting=md.GCC_PHAT)
        assert corr.shape == (1024,)

    def test_get_multiple_delays(self):
        ref = md.sine_wave(2048, freq=440.0, sample_rate=44100.0)
        sig1 = np.roll(ref, 3)
        sig2 = np.roll(ref, 7)
        delays = md.get_multiple_delays([ref, sig1, sig2], margin=20)
        assert delays.shape == (2,)
        assert abs(delays[0] - 3) <= 1
        assert abs(delays[1] - 7) <= 1


# ---------------------------------------------------------------------------
# Steganography
# ---------------------------------------------------------------------------

class TestSteganography:
    def test_steg_capacity(self):
        cap = md.steg_capacity(44100, sample_rate=44100.0, method=md.STEG_LSB)
        assert cap > 0

    def test_steg_text_roundtrip(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        message = "Hello, world!"
        stego, n = md.steg_encode(host, message, sample_rate=44100.0, method=md.STEG_LSB)
        assert n == len(message)
        recovered = md.steg_decode(stego, sample_rate=44100.0, method=md.STEG_LSB)
        assert recovered == message

    def test_steg_bytes_roundtrip(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        data = b"\x00\x01\x02\xff\xfe\xfd"
        stego, n = md.steg_encode_bytes(host, data, sample_rate=44100.0)
        assert n == len(data)
        recovered = md.steg_decode_bytes(stego, sample_rate=44100.0)
        assert recovered == data

    def test_steg_detect_lsb(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        stego, _ = md.steg_encode(host, "test", sample_rate=44100.0, method=md.STEG_LSB)
        method, ptype = md.steg_detect(stego, sample_rate=44100.0)
        assert method == md.STEG_LSB
        assert ptype == md.STEG_TYPE_TEXT


# ---------------------------------------------------------------------------
# Spectrogram text
# ---------------------------------------------------------------------------

class TestSpectrogramText:
    def test_spectrogram_text(self):
        sig = md.spectrogram_text("HI", freq_lo=200.0, freq_hi=7500.0,
                                  duration_sec=1.0, sample_rate=16000.0)
        assert len(sig) > 0
        assert sig.dtype == np.float64


# ---------------------------------------------------------------------------
# Biquad filter
# ---------------------------------------------------------------------------

class TestBiquad:
    def test_biquad_create(self):
        filt = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
        assert filt is not None

    def test_biquad_process(self):
        filt = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
        result = filt.process(1.0)
        assert isinstance(result, float)

    def test_biquad_process_array(self):
        filt = md.BiquadFilter(md.LPF, freq=1000.0, sample_rate=44100.0)
        sig = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
        out = filt.process_array(sig)
        assert out.shape == sig.shape

    def test_biquad_lowpass_attenuates_high_freq(self):
        filt = md.BiquadFilter(md.LPF, freq=500.0, sample_rate=44100.0)
        # 5000 Hz signal should be attenuated by a 500 Hz LPF
        high = md.sine_wave(4096, freq=5000.0, sample_rate=44100.0)
        out = filt.process_array(high)
        assert md.rms(out) < md.rms(high) * 0.5

    def test_all_filter_types(self):
        for ftype in [md.LPF, md.HPF, md.BPF, md.NOTCH, md.PEQ, md.LSH, md.HSH]:
            filt = md.BiquadFilter(ftype, freq=1000.0, sample_rate=44100.0,
                                   db_gain=6.0)
            assert filt is not None


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    def test_filter_type_constants(self):
        assert md.LPF == 0
        assert md.HPF == 1
        assert md.BPF == 2
        assert md.NOTCH == 3
        assert md.PEQ == 4
        assert md.LSH == 5
        assert md.HSH == 6

    def test_steg_constants(self):
        assert md.STEG_LSB == 0
        assert md.STEG_FREQ_BAND == 1

    def test_gcc_constants(self):
        assert md.GCC_SIMP == 0
        assert md.GCC_PHAT == 1
