#!/usr/bin/env python3
"""Generate interactive Plotly HTML plots for Sphinx documentation.

Python equivalent of miniDSP's ``examples/gen_signal_plots.c``.
Invoked automatically during the Sphinx build (via conf.py) or standalone::

    python docs/gen_signal_plots.py

Generated files are placed in ``docs/_static/plots/`` and embedded as
``<iframe>`` elements in the guide pages.
"""

import math
import os
import sys

import numpy as np

# Ensure pyminidsp is importable from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pyminidsp as md

# ---------------------------------------------------------------------------
# Signal parameters (match the C version exactly)
# ---------------------------------------------------------------------------
SAMPLE_RATE = 8192
N_SIGNAL = 8192

# STFT parameters
N_FFT = 256
HOP = 64

# Window visualisation
WINDOW_N = 256
WINDOW_FFT_VIS = 4096
FIR_TIME_SHOW = 512

# Pitch detection
PITCH_FRAME_N = 1024
PITCH_HOP = 128
PITCH_MIN_F0 = 80.0
PITCH_MAX_F0 = 400.0

# Mel/MFCC
MEL_FRAME_N = 1024
MEL_NUM_MELS = 26
MEL_NUM_COEFFS = 13
MEL_MIN_FREQ = 80.0
MEL_MAX_FREQ = 3900.0

# DTMF
DTMF_SAMPLE_RATE = 8000.0
DTMF_TONE_MS = 70
DTMF_PAUSE_MS = 70
DTMF_N_FFT = 256
DTMF_HOP = 8

# Spectrogram text
SPECTEXT_SAMPLE_RATE = 16000.0
SPECTEXT_N_FFT = 1024
SPECTEXT_HOP = 16

# Plotly CDN
PLOTLY_CDN = "https://cdn.plot.ly/plotly-2.35.2.min.js"


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------
def _head(title):
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '  <meta charset="utf-8">\n'
        f"  <title>{title}</title>\n"
        f'  <script src="{PLOTLY_CDN}"></script>\n'
        "  <style>\n"
        "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
        "    body { font-family: system-ui, -apple-system, sans-serif;"
        " background: #fafafa; }\n"
        "  </style>\n</head>\n<body>\n"
        '  <div id="plot"></div>\n  <script>\n'
    )


def _foot():
    return "  </script>\n</body>\n</html>\n"


def _js_array(name, values, fmt=".7g"):
    """Emit a JavaScript array literal."""
    items = ",".join(f"{v:{fmt}}" for v in values)
    return f"    const {name} = [{items}];\n"


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  {path}")


# ---------------------------------------------------------------------------
# Spectrum (dB magnitude vs frequency)
# ---------------------------------------------------------------------------
def write_spectrum_html(path, title, signal):
    num_bins = N_SIGNAL // 2 + 1
    mag = md.magnitude_spectrum(signal)

    # Single-sided amplitude normalization
    mag = mag / N_SIGNAL
    mag[1:-1] *= 2.0

    freqs = np.arange(num_bins)

    js = _head(title)
    js += f"    const freqs = Array.from({{length: {num_bins}}}, (_, k) => k);\n"
    js += _js_array("mags", mag)
    js += (
        "    const mags_db = mags.map(m => 20 * Math.log10(Math.max(m, 1e-6)));\n"
        "    Plotly.newPlot('plot', [{\n"
        "      x: freqs, y: mags_db,\n"
        "      type: 'scatter', mode: 'lines',\n"
        "      line: { color: '#2563eb', width: 1.2 },\n"
        "      hovertemplate: '%{x:.0f} Hz<br>%{y:.1f} dB<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Frequency (Hz)', range: [0, 4096] },\n"
        "      yaxis: { title: 'Magnitude (dB)', range: [-80, 5] },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Spectrogram (STFT heatmap)
# ---------------------------------------------------------------------------
def write_spectrogram_html(path, title, signal, n_fft=N_FFT, hop=HOP,
                           sample_rate=SAMPLE_RATE, y_range=None,
                           y_type="linear"):
    n = len(signal)
    num_bins = n_fft // 2 + 1
    num_frames = (n - n_fft) // hop + 1 if n >= n_fft else 0

    mag_flat = md.stft(signal, n_fft, hop)
    # Reshape: stft returns flat array [frame0_bin0, frame0_bin1, ..., frame1_bin0, ...]
    mag = mag_flat.reshape(num_frames, num_bins)

    time_step = hop / sample_rate
    freq_step = sample_rate / n_fft

    parts = [_head(title)]
    parts.append(f"    const times = Array.from({{length: {num_frames}}}, (_, f) => f * {time_step:.10g});\n")
    parts.append(f"    const freqs = Array.from({{length: {num_bins}}}, (_, k) => k * {freq_step:.10g});\n")

    # Z matrix: z[k][f] for Plotly heatmap (row=freq, col=time)
    z_rows = []
    for k in range(num_bins):
        row = mag[:, k] / n_fft
        row_db = 20.0 * np.log10(np.maximum(row, 1e-6))
        items = ",".join(f"{v:.1f}" for v in row_db)
        z_rows.append(f"      [{items}]")
    parts.append("    const z = [\n" + ",\n".join(z_rows) + "\n    ];\n")

    y_range_str = ""
    if y_range:
        y_range_str = f", range: {y_range}"

    y_type_str = ""
    if y_type != "linear":
        y_type_str = f", type: '{y_type}'"

    parts.append(
        "    Plotly.newPlot('plot', [{\n"
        "      type: 'heatmap',\n"
        "      x: times, y: freqs, z: z,\n"
        "      colorscale: 'Viridis',\n"
        "      zmin: -80, zmax: 0,\n"
        "      colorbar: { title: 'dB', thickness: 12 },\n"
        "      hovertemplate: 't: %{x:.3f} s<br>f: %{y:.0f} Hz<br>%{z:.1f} dB<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        f"      xaxis: {{ title: 'Time (s)' }},\n"
        f"      yaxis: {{ title: 'Frequency (Hz)'{y_type_str}{y_range_str} }},\n"
        "      margin: { t: 35, r: 80, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    parts.append(_foot())
    _write(path, "".join(parts))


# ---------------------------------------------------------------------------
# Window time-domain plot
# ---------------------------------------------------------------------------
def write_window_time_html(path, title, window):
    n = len(window)
    js = _head(title)
    js += f"    const idx = Array.from({{length: {n}}}, (_, i) => i);\n"
    js += _js_array("w", window, ".8g")
    js += (
        "    Plotly.newPlot('plot', [{\n"
        "      x: idx, y: w,\n"
        "      type: 'scatter', mode: 'lines',\n"
        "      line: { color: '#2563eb', width: 1.4 },\n"
        "      hovertemplate: 'n=%{x}<br>w[n]=%{y:.6f}<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        f"      xaxis: {{ title: 'Sample Index (n)', range: [0, {n - 1}] }},\n"
        "      yaxis: { title: 'Amplitude', range: [-0.05, 1.05] },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Window magnitude response (zero-padded FFT)
# ---------------------------------------------------------------------------
def write_window_spectrum_html(path, title, window, n_fft_vis):
    n_win = len(window)
    padded = np.zeros(n_fft_vis)
    padded[:n_win] = window

    mag = md.magnitude_spectrum(padded)
    num_bins = n_fft_vis // 2 + 1
    mag = mag / n_fft_vis
    mag[1:-1] *= 2.0

    js = _head(title)
    js += f"    const f = Array.from({{length: {num_bins}}}, (_, k) => k / {n_fft_vis}.0);\n"
    js += _js_array("mags", mag, ".8g")
    js += (
        "    const mags_db = mags.map(m => 20 * Math.log10(Math.max(m, 1e-6)));\n"
        "    Plotly.newPlot('plot', [{\n"
        "      x: f, y: mags_db,\n"
        "      type: 'scatter', mode: 'lines',\n"
        "      line: { color: '#2563eb', width: 1.2 },\n"
        "      hovertemplate: 'f: %{x:.4f} cycles/sample<br>%{y:.1f} dB<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Normalized Frequency (cycles/sample)', range: [0, 0.5] },\n"
        "      yaxis: { title: 'Magnitude (dB)', range: [-120, 5] },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Time-domain signal plot
# ---------------------------------------------------------------------------
def write_signal_time_html(path, title, signal, show_n):
    sig = signal[:show_n]
    ymin, ymax = float(sig.min()), float(sig.max())
    yrange = ymax - ymin
    pad = 0.10 * yrange if yrange > 1e-12 else 0.1
    ylo, yhi = ymin - pad, ymax + pad

    js = _head(title)
    js += f"    const idx = Array.from({{length: {show_n}}}, (_, i) => i);\n"
    js += _js_array("sig", sig, ".8g")
    js += (
        "    Plotly.newPlot('plot', [{\n"
        "      x: idx, y: sig,\n"
        "      type: 'scatter', mode: 'lines',\n"
        "      line: { color: '#059669', width: 1.3 },\n"
        "      hovertemplate: 'n=%{x}<br>x[n]=%{y:.6f}<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        f"      xaxis: {{ title: 'Sample Index (n)', range: [0, {show_n - 1}] }},\n"
        f"      yaxis: {{ title: 'Amplitude', range: [{ylo:.8g}, {yhi:.8g}] }},\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Pitch tracks (ground truth + ACF + FFT)
# ---------------------------------------------------------------------------
def write_pitch_tracks_html(path, title, times, truth, acf, fft):
    js = _head(title)
    js += _js_array("times", times, ".8g")
    js += _js_array("f0Truth", truth, ".8g")
    js += _js_array("f0Acf", acf, ".8g")
    js += _js_array("f0Fft", fft, ".8g")
    js += (
        "    Plotly.newPlot('plot', [\n"
        "      { x: times, y: f0Truth, name: 'Ground Truth', type: 'scatter', mode: 'lines',\n"
        "        line: { color: '#111827', width: 2.0 } },\n"
        "      { x: times, y: f0Acf, name: 'Autocorrelation F0', type: 'scatter', mode: 'lines+markers',\n"
        "        marker: { size: 4 }, line: { color: '#2563eb', width: 1.4 } },\n"
        "      { x: times, y: f0Fft, name: 'FFT F0', type: 'scatter', mode: 'lines+markers',\n"
        "        marker: { size: 4 }, line: { color: '#dc2626', width: 1.3 } }\n"
        "    ], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Time (s)' },\n"
        "      yaxis: { title: 'F0 (Hz)' },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360,\n"
        "      legend: { x: 1, y: 1, xanchor: 'right' }\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Pitch ACF peak plot
# ---------------------------------------------------------------------------
def write_pitch_acf_peak_html(path, title, acf_vals, lag_min, lag_max, selected_lag):
    lags = np.arange(lag_min, lag_max + 1, dtype=float)
    vals = acf_vals[lag_min:lag_max + 1]
    sel_idx = int(round(selected_lag))
    sel_val = float(acf_vals[sel_idx]) if lag_min <= sel_idx <= lag_max else 0.0

    js = _head(title)
    js += _js_array("lags", lags, ".8g")
    js += _js_array("acfVals", vals, ".8g")
    js += (
        "    Plotly.newPlot('plot', [\n"
        "      { x: lags, y: acfVals, name: 'Autocorrelation', type: 'scatter', mode: 'lines',\n"
        "        line: { color: '#2563eb', width: 1.4 } },\n"
        f"      {{ x: [{selected_lag:.8g}], y: [{sel_val:.8g}], name: 'Selected Lag', mode: 'markers',\n"
        "        marker: { color: '#dc2626', size: 9, symbol: 'diamond' } }\n"
        "    ], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Lag (samples)' },\n"
        "      yaxis: { title: 'Normalised R[lag]', range: [-1.1, 1.1] },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360,\n"
        "      legend: { x: 1, y: 1, xanchor: 'right' }\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Pitch FFT peak plot
# ---------------------------------------------------------------------------
def write_pitch_fft_peak_html(path, title, mag, num_bins, f0_hz):
    freqs = np.arange(num_bins, dtype=float) * SAMPLE_RATE / (2 * (num_bins - 1))
    mag_db = 20.0 * np.log10(np.maximum(mag, 1e-6))

    # Find the magnitude at the detected F0
    f0_bin = int(round(f0_hz * 2 * (num_bins - 1) / SAMPLE_RATE))
    f0_db = float(mag_db[f0_bin]) if 0 <= f0_bin < num_bins else -80.0

    js = _head(title)
    js += _js_array("freqs", freqs, ".8g")
    js += _js_array("magDb", mag_db, ".8g")
    js += (
        "    Plotly.newPlot('plot', [\n"
        "      { x: freqs, y: magDb, name: 'Magnitude', type: 'scatter', mode: 'lines',\n"
        "        line: { color: '#2563eb', width: 1.2 } },\n"
        f"      {{ x: [{f0_hz:.8g}], y: [{f0_db:.8g}], name: 'Detected F0', mode: 'markers',\n"
        "        marker: { color: '#dc2626', size: 9, symbol: 'diamond' } }\n"
        "    ], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Frequency (Hz)', range: [0, 1000] },\n"
        "      yaxis: { title: 'Magnitude (dB)' },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360,\n"
        "      legend: { x: 1, y: 1, xanchor: 'right' }\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Mel filterbank shapes
# ---------------------------------------------------------------------------
def write_mel_filterbank_html(path, title, filterbank, num_mels, frame_n, sr):
    num_bins = frame_n // 2 + 1
    freqs = np.arange(num_bins) * sr / frame_n
    # Plotly traces: one per mel filter
    colors = [f"hsl({int(i * 360 / num_mels)}, 70%, 50%)" for i in range(num_mels)]

    js = _head(title)
    js += _js_array("freqs", freqs, ".8g")

    fb = filterbank.reshape(num_mels, num_bins) if filterbank.ndim == 1 else filterbank

    js += "    const traces = [\n"
    for m in range(num_mels):
        row = fb[m]
        items = ",".join(f"{v.item():.6g}" for v in row)
        js += f"      {{ x: freqs, y: [{items}]"
        js += f", type: 'scatter', mode: 'lines', line: {{ color: '{colors[m]}', width: 1 }},\n"
        js += f"        name: 'Mel {m}', showlegend: false }},\n"
    js += "    ];\n"

    js += (
        "    Plotly.newPlot('plot', traces, {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Frequency (Hz)' },\n"
        "      yaxis: { title: 'Weight' },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Mel energies bar chart
# ---------------------------------------------------------------------------
def write_mel_energies_html(path, title, centers, energies):
    js = _head(title)
    js += _js_array("centers", centers, ".8g")
    js += _js_array("energies", energies, ".8g")
    js += (
        "    Plotly.newPlot('plot', [{\n"
        "      x: centers, y: energies,\n"
        "      type: 'bar',\n"
        "      marker: { color: '#2563eb' },\n"
        "      hovertemplate: 'Center: %{x:.0f} Hz<br>Energy: %{y:.4f}<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Center Frequency (Hz)' },\n"
        "      yaxis: { title: 'Energy' },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# MFCC bar chart
# ---------------------------------------------------------------------------
def write_mfcc_html(path, title, mfcc_vals):
    n = len(mfcc_vals)
    js = _head(title)
    js += f"    const idx = Array.from({{length: {n}}}, (_, i) => 'C' + i);\n"
    js += _js_array("vals", mfcc_vals, ".8g")
    js += (
        "    Plotly.newPlot('plot', [{\n"
        "      x: idx, y: vals,\n"
        "      type: 'bar',\n"
        "      marker: { color: '#059669' },\n"
        "      hovertemplate: '%{x}<br>%{y:.4f}<extra></extra>'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Coefficient' },\n"
        "      yaxis: { title: 'Value' },\n"
        "      margin: { t: 35, r: 20, b: 50, l: 60 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ---------------------------------------------------------------------------
# Difference plot (steganography)
# ---------------------------------------------------------------------------
def write_diff_html(path, title, host, stego, sr, show_n=2000):
    t = np.arange(show_n) / sr
    diff = host[:show_n] - stego[:show_n]

    js = _head(title)
    js += _js_array("t", t, ".6f")
    js += _js_array("diff", diff, ".8e")
    js += (
        "    Plotly.newPlot('plot', [{\n"
        "      x: t, y: diff,\n"
        "      type: 'scatter', mode: 'lines',\n"
        "      line: { width: 1, color: '#e74c3c' },\n"
        "      name: 'host - stego'\n"
        "    }], {\n"
        f"      title: {{ text: '{title}', font: {{ size: 13 }} }},\n"
        "      xaxis: { title: 'Time (s)' },\n"
        "      yaxis: { title: 'Amplitude', tickformat: '.1e' },\n"
        "      margin: { t: 35, r: 30, b: 50, l: 70 },\n"
        "      height: 360\n"
        "    }, { responsive: true });\n"
    )
    js += _foot()
    _write(path, js)


# ===========================================================================
# Main generation routine
# ===========================================================================
def generate(output_dir):
    """Generate all interactive Plotly HTML plots into *output_dir*."""

    def out(name):
        return os.path.join(output_dir, name)

    # ==================================================================
    # Phase 1: Signal generator spectra & spectrograms
    # ==================================================================
    print("Signal generator spectra & spectrograms:")

    generators = [
        ("sine", "Sine 440 Hz",
         md.sine_wave(N_SIGNAL, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)),
        ("square", "Square 440 Hz",
         md.square_wave(N_SIGNAL, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)),
        ("sawtooth", "Sawtooth 440 Hz",
         md.sawtooth_wave(N_SIGNAL, amplitude=0.8, freq=440.0, sample_rate=SAMPLE_RATE)),
        ("chirp_linear", "Linear Chirp 20-4000 Hz",
         md.chirp_linear(N_SIGNAL, amplitude=0.8, f_start=20.0, f_end=4000.0,
                         sample_rate=SAMPLE_RATE)),
        ("chirp_log", "Log Chirp 20-4000 Hz",
         md.chirp_log(N_SIGNAL, amplitude=0.8, f_start=20.0, f_end=4000.0,
                      sample_rate=SAMPLE_RATE)),
        ("white_noise", "White Noise (sigma=0.25)",
         md.white_noise(N_SIGNAL, amplitude=0.25, seed=42)),
    ]

    # Impulse train
    impulse = np.zeros(N_SIGNAL)
    for i in range(4):
        impulse[i * (N_SIGNAL // 4)] = 0.8
    generators.append(("impulse", "Impulse Train (4 clicks)", impulse))

    for name, label, sig in generators:
        write_spectrum_html(out(f"{name}_spectrum.html"), f"{label} - Spectrum", sig)
        write_spectrogram_html(out(f"{name}_spectrogram.html"), f"{label} - Spectrogram", sig)

    # ==================================================================
    # Phase 2: Simple effects spectrograms (before/after)
    # ==================================================================
    print("Simple effect spectrograms:")

    # Delay/echo: click train
    buf = np.zeros(N_SIGNAL)
    click_step = int(SAMPLE_RATE * 0.35)
    for i in range(0, N_SIGNAL, click_step):
        buf[i] = 0.9
    write_spectrogram_html(out("effect_delay_before_spectrogram.html"),
                           "Delay/Echo - Before (dry clicks) Spectrogram", buf)

    fx = md.delay_echo(buf, delay_samples=SAMPLE_RATE // 4, feedback=0.45,
                       dry=1.0, wet=0.6)
    write_spectrogram_html(out("effect_delay_after_spectrogram.html"),
                           "Delay/Echo - After Spectrogram", fx)

    # Tremolo: steady sine
    buf = md.sine_wave(N_SIGNAL, amplitude=0.8, freq=220.0, sample_rate=SAMPLE_RATE)
    write_spectrogram_html(out("effect_tremolo_before_spectrogram.html"),
                           "Tremolo - Before (220 Hz sine) Spectrogram", buf)

    fx = md.tremolo(buf, rate_hz=5.0, depth=0.8, sample_rate=SAMPLE_RATE)
    write_spectrogram_html(out("effect_tremolo_after_spectrogram.html"),
                           "Tremolo - After Spectrogram", fx)

    # Comb reverb: decaying burst
    buf = np.zeros(N_SIGNAL)
    burst_len = SAMPLE_RATE // 5
    for i in range(burst_len):
        env = math.exp(-6.0 * i / burst_len)
        buf[i] = 0.85 * env * math.sin(2.0 * math.pi * 330.0 * i / SAMPLE_RATE)
    write_spectrogram_html(out("effect_comb_before_spectrogram.html"),
                           "Comb Reverb - Before (decaying burst) Spectrogram", buf)

    fx = md.comb_reverb(buf, delay_samples=SAMPLE_RATE * 3 // 100, feedback=0.75,
                        dry=0.7, wet=0.6)
    write_spectrogram_html(out("effect_comb_after_spectrogram.html"),
                           "Comb Reverb - After Spectrogram", fx)

    # ==================================================================
    # Phase 3: Window function visuals
    # ==================================================================
    print("Window function visuals:")

    from pyminidsp._core import hann_window, hamming_window, blackman_window, rect_window

    hann = hann_window(WINDOW_N)
    hamming = hamming_window(WINDOW_N)
    blackman = blackman_window(WINDOW_N)
    rect = rect_window(WINDOW_N)

    for name, win in [("hann", hann), ("hamming", hamming),
                      ("blackman", blackman), ("rect", rect)]:
        label = {"hann": "Hanning", "hamming": "Hamming",
                 "blackman": "Blackman", "rect": "Rectangular"}[name]
        write_window_time_html(out(f"{name}_window_time.html"),
                               f"{label} Window - Time Domain", win)
        write_window_spectrum_html(out(f"{name}_window_spectrum.html"),
                                   f"{label} Window - Magnitude Response",
                                   win, WINDOW_FFT_VIS)

    # ==================================================================
    # Phase 4: FIR / convolution visuals
    # ==================================================================
    print("FIR/convolution visuals:")

    conv_kernel_len = 64
    conv_signal_len = N_SIGNAL - conv_kernel_len + 1

    # Impulse train input
    conv_in = np.zeros(conv_signal_len)
    for i in range(128, conv_signal_len, 512):
        conv_in[i] = 1.0
    conv_kernel = np.exp(-0.08 * np.arange(conv_kernel_len))

    result = md.convolution_time(conv_in, conv_kernel)
    write_signal_time_html(out("conv_time_response.html"),
                           "Time-Domain Convolution - Response", result, FIR_TIME_SHOW)
    # Pad/truncate to N_SIGNAL for spectrum
    padded = np.zeros(N_SIGNAL)
    padded[:min(len(result), N_SIGNAL)] = result[:N_SIGNAL]
    write_spectrum_html(out("conv_time_spectrum.html"),
                        "Time-Domain Convolution - Spectrum", padded)

    # Moving average: noisy square wave
    buf = md.square_wave(N_SIGNAL, amplitude=0.8, freq=220.0, sample_rate=SAMPLE_RATE)
    noise = md.white_noise(N_SIGNAL, amplitude=0.08, seed=123)
    buf = buf + noise
    result = md.moving_average(buf, window_len=16)
    write_signal_time_html(out("moving_average_response.html"),
                           "Moving-Average Filter - Response", result, FIR_TIME_SHOW)
    write_spectrum_html(out("moving_average_spectrum.html"),
                        "Moving-Average Filter - Spectrum", result)

    # General FIR filter
    fir_coeffs = np.array([0.05, 0.09, 0.12, 0.15, 0.18, 0.15, 0.12, 0.09, 0.05])
    result = md.fir_filter(buf, fir_coeffs)
    write_signal_time_html(out("fir_general_response.html"),
                           "General FIR Filter - Response", result, FIR_TIME_SHOW)
    write_spectrum_html(out("fir_general_spectrum.html"),
                        "General FIR Filter - Spectrum", result)

    # FFT overlap-add
    result = md.convolution_fft_ola(conv_in, conv_kernel)
    write_signal_time_html(out("conv_fft_ola_response.html"),
                           "FFT Overlap-Add Convolution - Response", result, FIR_TIME_SHOW)
    padded = np.zeros(N_SIGNAL)
    padded[:min(len(result), N_SIGNAL)] = result[:N_SIGNAL]
    write_spectrum_html(out("conv_fft_ola_spectrum.html"),
                        "FFT Overlap-Add Convolution - Spectrum", padded)

    # ==================================================================
    # Phase 5: Pitch detection visuals
    # ==================================================================
    print("Pitch detection visuals:")

    # Build voiced signal with piecewise F0
    noise = md.white_noise(N_SIGNAL, amplitude=0.08, seed=777)
    seg1 = N_SIGNAL // 3
    seg2 = 2 * N_SIGNAL // 3
    phase = 0.0
    buf = np.zeros(N_SIGNAL)
    for n in range(N_SIGNAL):
        f0 = 140.0 if n < seg1 else (220.0 if n < seg2 else 320.0)
        phase += 2.0 * math.pi * f0 / SAMPLE_RATE
        buf[n] = (0.75 * math.sin(phase)
                  + 0.22 * math.sin(2.0 * phase)
                  + 0.12 * math.sin(3.0 * phase)
                  + noise[n])

    # Frame-by-frame pitch estimation
    pitch_frames = (N_SIGNAL - PITCH_FRAME_N) // PITCH_HOP + 1
    pitch_t = np.zeros(pitch_frames)
    pitch_truth = np.zeros(pitch_frames)
    pitch_acf = np.zeros(pitch_frames)
    pitch_fft = np.zeros(pitch_frames)

    for f in range(pitch_frames):
        start = f * PITCH_HOP
        frame = buf[start:start + PITCH_FRAME_N]
        center = start + PITCH_FRAME_N // 2
        if center >= N_SIGNAL:
            center = N_SIGNAL - 1

        pitch_t[f] = center / SAMPLE_RATE
        pitch_truth[f] = 140.0 if center < seg1 else (220.0 if center < seg2 else 320.0)
        pitch_acf[f] = md.f0_autocorrelation(frame, sample_rate=SAMPLE_RATE,
                                              min_freq_hz=PITCH_MIN_F0, max_freq_hz=PITCH_MAX_F0)
        pitch_fft[f] = md.f0_fft(frame, sample_rate=SAMPLE_RATE,
                                  min_freq_hz=PITCH_MIN_F0, max_freq_hz=PITCH_MAX_F0)

    write_pitch_tracks_html(out("pitch_f0_tracks.html"),
                            "Pitch Detection - Ground Truth vs Estimated F0",
                            pitch_t, pitch_truth, pitch_acf, pitch_fft)

    # Single frame visualization (middle segment ~220 Hz)
    frame_idx = pitch_frames // 2
    frame = buf[frame_idx * PITCH_HOP:frame_idx * PITCH_HOP + PITCH_FRAME_N]

    lag_min = int(math.floor(SAMPLE_RATE / PITCH_MAX_F0))
    lag_max = int(math.ceil(SAMPLE_RATE / PITCH_MIN_F0))
    if lag_min < 1:
        lag_min = 1
    if lag_max > PITCH_FRAME_N - 1:
        lag_max = PITCH_FRAME_N - 1

    acf = md.autocorrelation(frame, max_lag=lag_max + 1)
    f0_acf_one = md.f0_autocorrelation(frame, sample_rate=SAMPLE_RATE,
                                        min_freq_hz=PITCH_MIN_F0, max_freq_hz=PITCH_MAX_F0)
    selected_lag = SAMPLE_RATE / f0_acf_one if f0_acf_one > 0 else 0.0
    write_pitch_acf_peak_html(out("pitch_acf_peak_frame.html"),
                              "Pitch Detection - Autocorrelation Peak (One Frame)",
                              acf, lag_min, lag_max, selected_lag)

    # FFT peak visualization
    num_bins = PITCH_FRAME_N // 2 + 1
    hann_win = hann_window(PITCH_FRAME_N)
    frame_win = frame * hann_win
    mag = md.magnitude_spectrum(frame_win)
    mag = mag / PITCH_FRAME_N
    mag[1:-1] *= 2.0
    f0_fft_one = md.f0_fft(frame, sample_rate=SAMPLE_RATE,
                            min_freq_hz=PITCH_MIN_F0, max_freq_hz=PITCH_MAX_F0)
    write_pitch_fft_peak_html(out("pitch_fft_peak_frame.html"),
                              "Pitch Detection - FFT Peak Pick (One Frame)",
                              mag, num_bins, f0_fft_one)

    # ==================================================================
    # Phase 6: Mel/MFCC visuals
    # ==================================================================
    print("Mel/MFCC visuals:")

    # Deterministic test signal
    t = np.arange(N_SIGNAL) / SAMPLE_RATE
    buf = 0.7 * np.sin(2 * np.pi * 440.0 * t) \
        + 0.2 * np.cos(2 * np.pi * 1000.0 * t) \
        + 0.1 * np.sin(2 * np.pi * 3000.0 * t)

    write_signal_time_html(out("mel_input_waveform.html"),
                           "Mel/MFCC Input Signal - Waveform", buf, 512)
    write_spectrogram_html(out("mel_input_spectrogram.html"),
                           "Mel/MFCC Input Signal - Spectrogram", buf)

    mel_frame = buf[:MEL_FRAME_N]

    # Mel filterbank
    fb = md.mel_filterbank(MEL_FRAME_N, sample_rate=SAMPLE_RATE,
                           num_mels=MEL_NUM_MELS)
    mel_bins = MEL_FRAME_N // 2 + 1
    write_mel_filterbank_html(out("mel_filterbank_shapes.html"),
                              "Mel Filterbank Shapes (HTK Mapping)",
                              fb, MEL_NUM_MELS, MEL_FRAME_N, SAMPLE_RATE)

    # Mel energies
    mel_vals = md.mel_energies(mel_frame, sample_rate=SAMPLE_RATE,
                               num_mels=MEL_NUM_MELS)
    # Compute center frequencies from filterbank
    fb_2d = fb.reshape(MEL_NUM_MELS, mel_bins) if fb.ndim == 1 else fb
    freq_axis = np.arange(mel_bins) * SAMPLE_RATE / MEL_FRAME_N
    centers = np.zeros(MEL_NUM_MELS)
    for m in range(MEL_NUM_MELS):
        row = fb_2d[m]
        total = row.sum()
        if total > 0:
            centers[m] = (freq_axis * row).sum() / total
    write_mel_energies_html(out("mel_energies_frame.html"),
                            "Mel Energies (One Frame Example)", centers, mel_vals)

    # MFCCs
    mfcc_vals = md.mfcc(mel_frame, sample_rate=SAMPLE_RATE,
                         num_mels=MEL_NUM_MELS, num_coeffs=MEL_NUM_COEFFS)
    write_mfcc_html(out("mfcc_frame.html"),
                    "MFCCs (One Frame, C0 Included)", mfcc_vals)

    # ==================================================================
    # Phase 7: DTMF spectrogram
    # ==================================================================
    print("DTMF spectrogram:")

    digits = "159#"
    dtmf_sig = md.dtmf_generate(digits, sample_rate=DTMF_SAMPLE_RATE,
                                 tone_ms=DTMF_TONE_MS, pause_ms=DTMF_PAUSE_MS)

    # Apply raised-cosine fade to each tone edge
    tone_samp = int(DTMF_TONE_MS * DTMF_SAMPLE_RATE / 1000)
    pause_samp = int(DTMF_PAUSE_MS * DTMF_SAMPLE_RATE / 1000)
    ramp = int(0.010 * DTMF_SAMPLE_RATE)
    if ramp > tone_samp // 2:
        ramp = tone_samp // 2
    off = 0
    for d in range(len(digits)):
        for i in range(ramp):
            g = 0.5 * (1.0 - math.cos(math.pi * i / ramp))
            dtmf_sig[off + i] *= g
            dtmf_sig[off + tone_samp - 1 - i] *= g
        off += tone_samp + pause_samp

    # Build DTMF spectrogram with reference lines
    dtmf_bins = DTMF_N_FFT // 2 + 1
    dtmf_frames = (len(dtmf_sig) - DTMF_N_FFT) // DTMF_HOP + 1

    dtmf_mag = md.stft(dtmf_sig, DTMF_N_FFT, DTMF_HOP)
    dtmf_mag = dtmf_mag.reshape(dtmf_frames, dtmf_bins)

    dtmf_time_step = DTMF_HOP / DTMF_SAMPLE_RATE
    dtmf_freq_step = DTMF_SAMPLE_RATE / DTMF_N_FFT

    parts = [_head('DTMF Sequence "159#" - Spectrogram')]
    parts.append(f"    const times = Array.from({{length: {dtmf_frames}}}, (_, f) => f * {dtmf_time_step:.10g});\n")
    parts.append(f"    const freqs = Array.from({{length: {dtmf_bins}}}, (_, k) => k * {dtmf_freq_step:.10g});\n")

    z_rows = []
    for k in range(dtmf_bins):
        row = dtmf_mag[:, k] / DTMF_N_FFT
        row_db = 20.0 * np.log10(np.maximum(row, 1e-6))
        items = ",".join(f"{v:.1f}" for v in row_db)
        z_rows.append(f"      [{items}]")
    parts.append("    const z = [\n" + ",\n".join(z_rows) + "\n    ];\n")

    parts.append(
        "    const dtmfFreqs = [\n"
        "      {f: 697,  label: '697 Hz'},  {f: 770,  label: '770 Hz'},\n"
        "      {f: 852,  label: '852 Hz'},  {f: 941,  label: '941 Hz'},\n"
        "      {f: 1209, label: '1209 Hz'}, {f: 1336, label: '1336 Hz'},\n"
        "      {f: 1477, label: '1477 Hz'}, {f: 1633, label: '1633 Hz'}\n"
        "    ];\n"
        "    const shapes = dtmfFreqs.map(d => ({\n"
        "      type: 'line', xref: 'paper', x0: 0, x1: 1,\n"
        "      yref: 'y', y0: d.f, y1: d.f,\n"
        "      line: { color: 'rgba(255,255,255,0.5)', width: 1, dash: 'dot' }\n"
        "    }));\n"
        "    const annotations = dtmfFreqs.map(d => ({\n"
        "      xref: 'paper', x: 1.01, yref: 'y', y: d.f,\n"
        "      text: d.label, showarrow: false,\n"
        "      font: { size: 9, color: '#666' }, xanchor: 'left'\n"
        "    }));\n"
        "    Plotly.newPlot('plot', [{\n"
        "      type: 'heatmap',\n"
        "      x: times, y: freqs, z: z,\n"
        "      colorscale: 'Viridis',\n"
        "      zmin: -80, zmax: 0,\n"
        "      colorbar: { title: 'dB', thickness: 12 },\n"
        "      hovertemplate: 't: %{x:.3f} s<br>f: %{y:.0f} Hz<br>%{z:.1f} dB<extra></extra>'\n"
        "    }], {\n"
        '      title: { text: \'DTMF Sequence "159#" - Spectrogram\', font: { size: 13 } },\n'
        "      xaxis: { title: 'Time (s)' },\n"
        "      yaxis: { title: 'Frequency (Hz)', range: [0, 2000] },\n"
        "      margin: { t: 35, r: 80, b: 50, l: 60 },\n"
        "      height: 360,\n"
        "      shapes: shapes,\n"
        "      annotations: annotations\n"
        "    }, { responsive: true });\n"
    )
    parts.append(_foot())
    _write(out("dtmf_spectrogram.html"), "".join(parts))

    # ==================================================================
    # Phase 8: Spectrogram text
    # ==================================================================
    print("Spectrogram text:")

    st_dur = 2.25
    st_pad = 0.5
    st_text = md.spectrogram_text("HELLO", freq_lo=400.0, freq_hi=7300.0,
                                   duration_sec=st_dur, sample_rate=SPECTEXT_SAMPLE_RATE)
    st_pad_samp = int(st_pad * SPECTEXT_SAMPLE_RATE)
    st_sig = np.concatenate([np.zeros(st_pad_samp), st_text, np.zeros(st_pad_samp)])

    write_spectrogram_html(out("spectext_hello_spectrogram.html"),
                           'Spectrogram Text "HELLO"', st_sig,
                           n_fft=SPECTEXT_N_FFT, hop=SPECTEXT_HOP,
                           sample_rate=SPECTEXT_SAMPLE_RATE,
                           y_range="[0, 8000]")

    # ==================================================================
    # Phase 9: Shepard tone spectrograms
    # ==================================================================
    print("Shepard tone spectrograms:")

    shep_sr = 44100.0
    shep_dur = 5.0
    shep_n = int(shep_sr * shep_dur)
    shep_fft = 2048
    shep_hop = 512

    for rate, label, fname in [(0.5, "Rising", "shepard_rising_spectrogram.html"),
                                (-0.5, "Falling", "shepard_falling_spectrogram.html")]:
        sig = md.shepard_tone(shep_n, amplitude=0.8, base_freq=440.0,
                              sample_rate=shep_sr, rate_octaves_per_sec=rate,
                              num_octaves=8)
        write_spectrogram_html(out(fname),
                               f"Shepard Tone ({label} 0.5 oct/s)", sig,
                               n_fft=shep_fft, hop=shep_hop, sample_rate=shep_sr,
                               y_range="[Math.log10(30), Math.log10(10000)]",
                               y_type="log")

    md.shutdown()

    # ==================================================================
    # Phase 10: Steganography plots
    # ==================================================================
    print("Steganography plots:")

    steg_sr = 44100.0
    steg_n = int(steg_sr * 3.0)
    secret = "Hidden message inside audio!"

    host = md.sine_wave(steg_n, amplitude=0.8, freq=440.0, sample_rate=steg_sr)
    stego_lsb, _ = md.steg_encode(host, secret, sample_rate=steg_sr,
                                    method=md.STEG_LSB)
    stego_freq, _ = md.steg_encode(host, secret, sample_rate=steg_sr,
                                     method=md.STEG_FREQ_BAND)

    # LSB difference
    write_diff_html(out("steg_lsb_diff.html"),
                    "LSB Steganography \\u2014 Difference Signal",
                    host, stego_lsb, steg_sr)

    # Freq-band spectrogram (first 0.5 s)
    spec_dur_samp = int(0.5 * steg_sr)
    write_spectrogram_html(out("steg_freq_spectrogram.html"),
                           "Frequency-Band Stego (BFSK at 18.5/19.5 kHz)",
                           stego_freq[:spec_dur_samp],
                           n_fft=2048, hop=64, sample_rate=steg_sr)

    md.shutdown()
    print("Done.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "_static", "plots")
    generate(output_dir)
