"""
CFFI build script for the miniDSP C library.

This script compiles the miniDSP C library into a shared library that can
be loaded by the Python bindings. It is invoked automatically when the
package is installed, or can be run manually:

    python pyminidsp/_build_minidsp.py

Prerequisites:
    - FFTW3 development headers and library (libfftw3-dev on Debian/Ubuntu)
    - A C compiler (gcc or clang)
"""

import cffi
import os
import subprocess
import sys

ffibuilder = cffi.FFI()

# C declarations visible to Python (no #includes, just the API surface)
ffibuilder.cdef("""
    /* === minidsp.h === */

    /* Basic signal measurement */
    double MD_dot(const double *a, const double *b, unsigned N);
    double MD_entropy(const double *a, unsigned N, _Bool clip);
    double MD_energy(const double *a, unsigned N);
    double MD_power(const double *a, unsigned N);
    double MD_power_db(const double *a, unsigned N);

    /* Signal analysis */
    double MD_rms(const double *a, unsigned N);
    double MD_zero_crossing_rate(const double *a, unsigned N);
    void MD_autocorrelation(const double *a, unsigned N,
                            double *out, unsigned max_lag);
    void MD_peak_detect(const double *a, unsigned N, double threshold,
                        unsigned min_distance, unsigned *peaks_out,
                        unsigned *num_peaks_out);
    double MD_f0_autocorrelation(const double *signal, unsigned N,
                                 double sample_rate,
                                 double min_freq_hz, double max_freq_hz);
    double MD_f0_fft(const double *signal, unsigned N,
                     double sample_rate,
                     double min_freq_hz, double max_freq_hz);
    void MD_mix(const double *a, const double *b, double *out,
                unsigned N, double w_a, double w_b);

    /* Simple effects */
    void MD_delay_echo(const double *in, double *out, unsigned N,
                       unsigned delay_samples, double feedback,
                       double dry, double wet);
    void MD_tremolo(const double *in, double *out, unsigned N,
                    double rate_hz, double depth, double sample_rate);
    void MD_comb_reverb(const double *in, double *out, unsigned N,
                        unsigned delay_samples, double feedback,
                        double dry, double wet);

    /* FIR filters / convolution */
    unsigned MD_convolution_num_samples(unsigned signal_len, unsigned kernel_len);
    void MD_convolution_time(const double *signal, unsigned signal_len,
                             const double *kernel, unsigned kernel_len,
                             double *out);
    void MD_moving_average(const double *signal, unsigned signal_len,
                           unsigned window_len, double *out);
    void MD_fir_filter(const double *signal, unsigned signal_len,
                       const double *coeffs, unsigned num_taps,
                       double *out);
    void MD_convolution_fft_ola(const double *signal, unsigned signal_len,
                                const double *kernel, unsigned kernel_len,
                                double *out);

    /* Signal scaling */
    double MD_scale(double in,
                    double oldmin, double oldmax,
                    double newmin, double newmax);
    void MD_scale_vec(double *in, double *out, unsigned N,
                      double oldmin, double oldmax,
                      double newmin, double newmax);
    void MD_fit_within_range(double *in, double *out, unsigned N,
                             double newmin, double newmax);
    void MD_adjust_dblevel(const double *in, double *out,
                           unsigned N, double dblevel);

    /* FFT / Spectrum analysis */
    void MD_magnitude_spectrum(const double *signal, unsigned N, double *mag_out);
    void MD_power_spectral_density(const double *signal, unsigned N, double *psd_out);
    void MD_phase_spectrum(const double *signal, unsigned N, double *phase_out);
    unsigned MD_stft_num_frames(unsigned signal_len, unsigned N, unsigned hop);
    void MD_stft(const double *signal, unsigned signal_len,
                 unsigned N, unsigned hop,
                 double *mag_out);
    void MD_mel_filterbank(unsigned N, double sample_rate,
                           unsigned num_mels,
                           double min_freq_hz, double max_freq_hz,
                           double *filterbank_out);
    void MD_mel_energies(const double *signal, unsigned N,
                         double sample_rate, unsigned num_mels,
                         double min_freq_hz, double max_freq_hz,
                         double *mel_out);
    void MD_mfcc(const double *signal, unsigned N,
                 double sample_rate,
                 unsigned num_mels, unsigned num_coeffs,
                 double min_freq_hz, double max_freq_hz,
                 double *mfcc_out);

    /* Window generation */
    void MD_Gen_Hann_Win(double *out, unsigned n);
    void MD_Gen_Hamming_Win(double *out, unsigned n);
    void MD_Gen_Blackman_Win(double *out, unsigned n);
    void MD_Gen_Rect_Win(double *out, unsigned n);

    /* Signal generators */
    void MD_sine_wave(double *output, unsigned N, double amplitude,
                      double freq, double sample_rate);
    void MD_white_noise(double *output, unsigned N, double amplitude,
                        unsigned seed);
    void MD_impulse(double *output, unsigned N, double amplitude, unsigned position);
    void MD_chirp_linear(double *output, unsigned N, double amplitude,
                         double f_start, double f_end, double sample_rate);
    void MD_chirp_log(double *output, unsigned N, double amplitude,
                      double f_start, double f_end, double sample_rate);
    void MD_square_wave(double *output, unsigned N, double amplitude,
                        double freq, double sample_rate);
    void MD_sawtooth_wave(double *output, unsigned N, double amplitude,
                          double freq, double sample_rate);
    void MD_shepard_tone(double *output, unsigned N, double amplitude,
                         double base_freq, double sample_rate,
                         double rate_octaves_per_sec, unsigned num_octaves);

    /* DTMF */
    typedef struct {
        char   digit;
        double start_s;
        double end_s;
    } MD_DTMFTone;

    unsigned MD_dtmf_detect(const double *signal, unsigned signal_len,
                            double sample_rate,
                            MD_DTMFTone *tones_out, unsigned max_tones);
    void MD_dtmf_generate(double *output, const char *digits,
                          double sample_rate,
                          unsigned tone_ms, unsigned pause_ms);
    unsigned MD_dtmf_signal_length(unsigned num_digits, double sample_rate,
                                   unsigned tone_ms, unsigned pause_ms);

    /* Resource cleanup */
    void MD_shutdown(void);

    /* GCC delay estimation */
    void MD_get_multiple_delays(const double **sigs, unsigned M, unsigned N,
                                unsigned margin, int weightfunc,
                                int *outdelays);
    int MD_get_delay(const double *siga, const double *sigb, unsigned N,
                     double *ent, unsigned margin, int weightfunc);
    void MD_gcc(const double *siga, const double *sigb, unsigned N,
                double *lagvals, int weightfunc);

    /* Spectrogram text */
    unsigned MD_spectrogram_text(double *output, unsigned max_len,
                                 const char *text,
                                 double freq_lo, double freq_hi,
                                 double duration_sec, double sample_rate);

    /* Steganography */
    unsigned MD_steg_capacity(unsigned signal_len, double sample_rate, int method);
    unsigned MD_steg_encode(const double *host, double *output,
                            unsigned signal_len, double sample_rate,
                            const char *message, int method);
    unsigned MD_steg_decode(const double *stego, unsigned signal_len,
                            double sample_rate,
                            char *message_out, unsigned max_msg_len,
                            int method);
    unsigned MD_steg_encode_bytes(const double *host, double *output,
                                  unsigned signal_len, double sample_rate,
                                  const unsigned char *data, unsigned data_len,
                                  int method);
    unsigned MD_steg_decode_bytes(const double *stego, unsigned signal_len,
                                  double sample_rate,
                                  unsigned char *data_out, unsigned max_len,
                                  int method);
    int MD_steg_detect(const double *signal, unsigned signal_len,
                       double sample_rate, int *payload_type_out);

    /* === biquad.h === */
    typedef double smp_type;

    typedef struct {
        smp_type a0, a1, a2, a3, a4;
        smp_type x1, x2;
        smp_type y1, y2;
    } biquad;

    smp_type BiQuad(smp_type sample, biquad *b);
    biquad *BiQuad_new(int type, smp_type dbGain,
                       smp_type freq, smp_type srate,
                       smp_type bandwidth);
    void free(void *ptr);
""")

# Locate the miniDSP source directory
_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)

# Look for the miniDSP source in priority order:
# 1. MINIDSP_SRC env var (explicit override)
# 2. vendor/miniDSP/ (bundled in sdist for PyPI installs)
# 3. Adjacent miniDSP/ dirs and /tmp (dev convenience)
_search_paths = [
    os.environ.get("MINIDSP_SRC", ""),
    os.path.join(_project_root, "vendor", "miniDSP"),
    os.path.join(_this_dir, "..", "miniDSP"),
    os.path.join(_this_dir, "..", "..", "miniDSP"),
    "/tmp/miniDSP",
]

_minidsp_src = None
for p in _search_paths:
    if p and os.path.isdir(p) and os.path.isfile(os.path.join(p, "include", "minidsp.h")):
        _minidsp_src = os.path.abspath(p)
        break

if _minidsp_src is None:
    print(
        "ERROR: miniDSP C source not found.\n"
        "Provide it via one of:\n"
        "  1. Set MINIDSP_SRC env var: MINIDSP_SRC=/path/to/miniDSP pip install .\n"
        "  2. Place it at vendor/miniDSP/ relative to the project root\n"
        "  3. Clone it adjacent to this repo: git clone https://github.com/wooters/miniDSP.git",
        file=sys.stderr,
    )
    sys.exit(1)

print(f"Using miniDSP source from: {_minidsp_src}")

# Source files to compile (excluding fileio.c and liveio.c which need
# libsndfile and portaudio respectively — those are optional)
_core_sources = [
    "src/minidsp_core.c",
    "src/minidsp_generators.c",
    "src/minidsp_spectrum.c",
    "src/minidsp_fir.c",
    "src/minidsp_dtmf.c",
    "src/minidsp_spectext.c",
    "src/minidsp_steg.c",
    "src/minidsp_gcc.c",
    "src/biquad.c",
]

_source_paths = [os.path.relpath(os.path.join(_minidsp_src, s)) for s in _core_sources]

# Detect Homebrew prefix on macOS
_extra_include = []
_extra_lib = []
try:
    brew_prefix = subprocess.check_output(
        ["brew", "--prefix"], stderr=subprocess.DEVNULL
    ).decode().strip()
    _extra_include.append(os.path.join(brew_prefix, "include"))
    _extra_lib.append(os.path.join(brew_prefix, "lib"))
except (FileNotFoundError, subprocess.CalledProcessError):
    pass

ffibuilder.set_source(
    "pyminidsp._minidsp_cffi",
    """
    #include "minidsp.h"
    #include "biquad.h"
    """,
    sources=_source_paths,
    include_dirs=[os.path.relpath(os.path.join(_minidsp_src, "include"))] + _extra_include,
    library_dirs=_extra_lib,
    libraries=["fftw3", "m"],
    extra_compile_args=["-std=c2x", "-O2"],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
