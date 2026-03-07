"""Tests for DTMF tone generation and detection."""

import numpy as np
import pytest

import pyminidsp as md


class TestDtmfSignalLength:
    def test_positive(self):
        length = md.dtmf_signal_length(3, sample_rate=8000.0, tone_ms=70, pause_ms=70)
        assert length > 0

    def test_consistency(self):
        len3 = md.dtmf_signal_length(3, sample_rate=8000.0, tone_ms=70, pause_ms=70)
        len6 = md.dtmf_signal_length(6, sample_rate=8000.0, tone_ms=70, pause_ms=70)
        assert len6 > len3


class TestDtmfRoundtrip:
    def test_basic(self):
        digits = "5551234"
        sig = md.dtmf_generate(digits, sample_rate=8000.0)
        detected = md.dtmf_detect(sig, sample_rate=8000.0)
        detected_digits = "".join(t[0] for t in detected)
        assert detected_digits == digits

    def test_full_character_set(self):
        digits = "0123456789ABCD*#"
        sig = md.dtmf_generate(digits, sample_rate=8000.0)
        detected = md.dtmf_detect(sig, sample_rate=8000.0)
        detected_digits = "".join(t[0] for t in detected)
        assert detected_digits == digits

    def test_single_digit(self):
        for d in "0123456789ABCD*#":
            sig = md.dtmf_generate(d, sample_rate=8000.0)
            detected = md.dtmf_detect(sig, sample_rate=8000.0)
            assert len(detected) == 1
            assert detected[0][0] == d


class TestDtmfTiming:
    def test_timing(self):
        sig = md.dtmf_generate("1", sample_rate=8000.0, tone_ms=70, pause_ms=70)
        tones = md.dtmf_detect(sig, sample_rate=8000.0)
        assert len(tones) == 1
        assert tones[0][0] == "1"
        assert tones[0][1] >= 0.0  # start_s

    def test_signal_length_matches(self):
        digits = "123"
        expected_len = md.dtmf_signal_length(len(digits), sample_rate=8000.0,
                                              tone_ms=70, pause_ms=70)
        sig = md.dtmf_generate(digits, sample_rate=8000.0, tone_ms=70, pause_ms=70)
        assert len(sig) == expected_len
