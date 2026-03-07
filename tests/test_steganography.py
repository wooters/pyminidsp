"""Tests for audio steganography."""

import numpy as np
import pytest

import pyminidsp as md


class TestStegCapacity:
    def test_positive(self):
        cap = md.steg_capacity(44100, sample_rate=44100.0, method=md.STEG_LSB)
        assert cap > 0

    def test_lsb_vs_freq_band(self):
        cap_lsb = md.steg_capacity(44100, sample_rate=44100.0, method=md.STEG_LSB)
        cap_fb = md.steg_capacity(44100, sample_rate=44100.0, method=md.STEG_FREQ_BAND)
        # Both should be positive; LSB typically has higher capacity
        assert cap_lsb > 0
        assert cap_fb > 0


class TestStegTextLSB:
    def test_roundtrip(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        message = "Hello, world!"
        stego, n = md.steg_encode(host, message, sample_rate=44100.0, method=md.STEG_LSB)
        assert n == len(message)
        recovered = md.steg_decode(stego, sample_rate=44100.0, method=md.STEG_LSB)
        assert recovered == message

    def test_detect(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        stego, _ = md.steg_encode(host, "test", sample_rate=44100.0, method=md.STEG_LSB)
        method, ptype = md.steg_detect(stego, sample_rate=44100.0)
        assert method == md.STEG_LSB
        assert ptype == md.STEG_TYPE_TEXT


class TestStegTextFreqBand:
    def test_roundtrip(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        message = "Hi"
        stego, n = md.steg_encode(host, message, sample_rate=44100.0,
                                   method=md.STEG_FREQ_BAND)
        assert n == len(message)
        recovered = md.steg_decode(stego, sample_rate=44100.0, method=md.STEG_FREQ_BAND)
        assert recovered == message

    def test_detect(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        stego, _ = md.steg_encode(host, "AB", sample_rate=44100.0,
                                   method=md.STEG_FREQ_BAND)
        method, ptype = md.steg_detect(stego, sample_rate=44100.0)
        assert method == md.STEG_FREQ_BAND
        assert ptype == md.STEG_TYPE_TEXT


class TestStegBytesLSB:
    def test_roundtrip(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        data = b"\x00\x01\x02\xff\xfe\xfd"
        stego, n = md.steg_encode_bytes(host, data, sample_rate=44100.0)
        assert n == len(data)
        recovered = md.steg_decode_bytes(stego, sample_rate=44100.0)
        assert recovered == data


class TestStegBytesFreqBand:
    def test_roundtrip(self):
        host = md.sine_wave(44100, amplitude=0.8, freq=440.0, sample_rate=44100.0)
        data = b"\xAA\xBB"
        stego, n = md.steg_encode_bytes(host, data, sample_rate=44100.0,
                                         method=md.STEG_FREQ_BAND)
        assert n == len(data)
        recovered = md.steg_decode_bytes(stego, sample_rate=44100.0,
                                          method=md.STEG_FREQ_BAND)
        assert recovered == data


class TestStegConstants:
    def test_values(self):
        assert md.STEG_LSB == 0
        assert md.STEG_FREQ_BAND == 1
