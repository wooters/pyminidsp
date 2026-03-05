#!/usr/bin/env python3
"""Generate WAV audio samples for the Sphinx documentation.

This is the Python equivalent of miniDSP's ``examples/gen_audio_samples.c``.
It is invoked automatically during the Sphinx build (via conf.py) or can be
run standalone::

    python docs/gen_audio_samples.py

Generated files are placed in ``docs/_static/audio/`` and embedded as
``<audio>`` elements in the guide pages.
"""

import math
import os
import struct
import sys
import wave

# Ensure pyminidsp is importable from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SAMPLE_RATE = 44100
DURATION = 2.0


def write_wav(path, samples, sample_rate=SAMPLE_RATE):
    """Write a list/array of float64 samples to a 16-bit PCM WAV file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        data = b""
        for s in samples:
            s = max(-1.0, min(1.0, s))
            data += struct.pack("<h", int(s * 32767))
        wf.writeframes(data)


def generate(output_dir):
    """Generate all audio samples into *output_dir*."""
    import numpy as np

    import pyminidsp as md

    N = int(SAMPLE_RATE * DURATION)

    def out(name):
        return os.path.join(output_dir, name)

    print(f"Generating audio samples ({N} samples, {SAMPLE_RATE} Hz, {DURATION}s):")

    # ------------------------------------------------------------------
    # Signal generators
    # ------------------------------------------------------------------

    # Sine wave — 440 Hz
    sig = md.sine_wave(N, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)
    write_wav(out("sine_440hz.wav"), sig)
    print(f"  {out('sine_440hz.wav')}")

    # Square wave — 440 Hz
    sig = md.square_wave(N, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)
    write_wav(out("square_440hz.wav"), sig)
    print(f"  {out('square_440hz.wav')}")

    # Sawtooth wave — 440 Hz
    sig = md.sawtooth_wave(N, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)
    write_wav(out("sawtooth_440hz.wav"), sig)
    print(f"  {out('sawtooth_440hz.wav')}")

    # Linear chirp — 20 Hz to 4000 Hz
    sig = md.chirp_linear(N, amplitude=0.8, f_start=20.0, f_end=4000.0,
                          sample_rate=SAMPLE_RATE)
    write_wav(out("chirp_linear.wav"), sig)
    print(f"  {out('chirp_linear.wav')}")

    # Logarithmic chirp — 20 Hz to 4000 Hz
    sig = md.chirp_log(N, amplitude=0.8, f_start=20.0, f_end=4000.0,
                       sample_rate=SAMPLE_RATE)
    write_wav(out("chirp_log.wav"), sig)
    print(f"  {out('chirp_log.wav')}")

    # White noise — seed 42
    sig = md.white_noise(N, amplitude=0.25, seed=42)
    write_wav(out("white_noise.wav"), sig)
    print(f"  {out('white_noise.wav')}")

    # Impulse train — 4 clicks at 0.5s intervals
    sig = np.zeros(N)
    for i in range(4):
        pos = int(i * 0.5 * SAMPLE_RATE)
        if pos < N:
            sig[pos] = 0.8
    write_wav(out("impulse_train.wav"), sig)
    print(f"  {out('impulse_train.wav')}")

    # ------------------------------------------------------------------
    # Simple effects: before/after clips
    # ------------------------------------------------------------------

    # Delay source: percussive click train
    buf = np.zeros(N)
    step = int(0.35 * SAMPLE_RATE)
    for i in range(0, N, step):
        buf[i] = 0.9
    write_wav(out("effect_delay_before.wav"), buf)
    print(f"  {out('effect_delay_before.wav')}")

    fx = md.delay_echo(buf, delay_samples=11025, feedback=0.45, dry=1.0, wet=0.6)
    write_wav(out("effect_delay_after.wav"), fx)
    print(f"  {out('effect_delay_after.wav')}")

    # Tremolo source: steady 220 Hz sine
    buf = md.sine_wave(N, amplitude=0.8, freq=220.0, sample_rate=SAMPLE_RATE)
    write_wav(out("effect_tremolo_before.wav"), buf)
    print(f"  {out('effect_tremolo_before.wav')}")

    fx = md.tremolo(buf, rate_hz=5.0, depth=0.8, sample_rate=SAMPLE_RATE)
    write_wav(out("effect_tremolo_after.wav"), fx)
    print(f"  {out('effect_tremolo_after.wav')}")

    # Comb source: short decaying tone burst
    buf = np.zeros(N)
    burst_len = SAMPLE_RATE // 5  # 200 ms
    for i in range(burst_len):
        env = math.exp(-6.0 * i / burst_len)
        buf[i] = 0.85 * env * math.sin(2.0 * math.pi * 330.0 * i / SAMPLE_RATE)
    write_wav(out("effect_comb_before.wav"), buf)
    print(f"  {out('effect_comb_before.wav')}")

    fx = md.comb_reverb(buf, delay_samples=1323, feedback=0.75, dry=0.7, wet=0.6)
    write_wav(out("effect_comb_after.wav"), fx)
    print(f"  {out('effect_comb_after.wav')}")

    # ------------------------------------------------------------------
    # Spectrogram text: "HELLO" at 16 kHz
    # ------------------------------------------------------------------
    st_sr = 16000
    st_dur = 2.25
    st_pad = 0.5
    st_max = int(st_sr * st_dur) + 1024
    st_text = md.spectrogram_text("HELLO", freq_lo=400.0, freq_hi=7300.0,
                                  duration_sec=st_dur, sample_rate=st_sr)
    # Pad with silence before and after
    st_pad_samp = int(st_pad * st_sr)
    padded = np.concatenate([np.zeros(st_pad_samp), st_text, np.zeros(st_pad_samp)])
    write_wav(out("spectrogram_text_hello.wav"), padded, sample_rate=st_sr)
    print(f"  {out('spectrogram_text_hello.wav')}")

    # ------------------------------------------------------------------
    # Shepard tones: rising, falling, and static (5 seconds at 44100 Hz)
    # ------------------------------------------------------------------
    shep_n = int(SAMPLE_RATE * 5.0)

    sig = md.shepard_tone(shep_n, amplitude=0.8, base_freq=440.0,
                          sample_rate=SAMPLE_RATE, rate_octaves_per_sec=0.5,
                          num_octaves=8)
    write_wav(out("shepard_rising.wav"), sig)
    print(f"  {out('shepard_rising.wav')}")

    sig = md.shepard_tone(shep_n, amplitude=0.8, base_freq=440.0,
                          sample_rate=SAMPLE_RATE, rate_octaves_per_sec=-0.5,
                          num_octaves=8)
    write_wav(out("shepard_falling.wav"), sig)
    print(f"  {out('shepard_falling.wav')}")

    sig = md.shepard_tone(shep_n, amplitude=0.8, base_freq=440.0,
                          sample_rate=SAMPLE_RATE, rate_octaves_per_sec=0.0,
                          num_octaves=8)
    write_wav(out("shepard_static.wav"), sig)
    print(f"  {out('shepard_static.wav')}")

    # ------------------------------------------------------------------
    # Audio steganography: host, LSB stego, and freq-band stego
    # ------------------------------------------------------------------
    steg_n = int(SAMPLE_RATE * 3.0)
    secret = "Hidden message inside audio!"

    host = md.sine_wave(steg_n, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)
    write_wav(out("steg_host.wav"), host)
    print(f"  {out('steg_host.wav')}")

    stego, n = md.steg_encode(host, secret, sample_rate=SAMPLE_RATE,
                              method=md.STEG_LSB)
    write_wav(out("steg_lsb.wav"), stego)
    print(f"  {out('steg_lsb.wav')}")

    stego, n = md.steg_encode(host, secret, sample_rate=SAMPLE_RATE,
                              method=md.STEG_FREQ_BAND)
    write_wav(out("steg_freq.wav"), stego)
    print(f"  {out('steg_freq.wav')}")

    md.shutdown()
    print("Done.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "_static", "audio")
    generate(output_dir)
