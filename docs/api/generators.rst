Signal Generators
=================

Stateless utilities that create test signals without requiring audio
input.  All generators return NumPy ``float64`` arrays.

.. autofunction:: pyminidsp.sine_wave

   Generate a pure sine tone:

   .. math::

      x[n] = A \sin(2\pi f \, n / f_s)

   The simplest test signal in DSP.  Use it to verify filter responses,
   check FFT bin alignment, or provide a clean input for any processing
   chain.

   :param n: Number of samples.
   :param amplitude: Peak amplitude (e.g. 1.0).
   :param freq: Frequency in Hz.
   :param sample_rate: Sampling rate in Hz.

   .. code-block:: python

      signal = md.sine_wave(44100, amplitude=1.0, freq=440.0, sample_rate=44100.0)

.. autofunction:: pyminidsp.white_noise

   Generate Gaussian white noise via the Box-Muller transform.  White
   noise has equal energy at all frequencies — its power spectral density
   is approximately flat.

   Use white noise to test filters, measure impulse responses, or as an
   additive noise source for SNR experiments.

   :param n: Number of samples.
   :param amplitude: Standard deviation of the noise.
   :param seed: Random seed for reproducibility.

   .. code-block:: python

      noise = md.white_noise(4096, amplitude=1.0, seed=42)

.. autofunction:: pyminidsp.impulse

   Generate a discrete impulse (Kronecker delta).  The output is all
   zeros except at *position*, where the value is *amplitude*.

   The unit impulse (amplitude 1.0 at position 0) is the identity
   element of convolution and has a perfectly flat magnitude spectrum.

   Common uses:

   - Measure a system's impulse response by feeding it through a filter.
   - Verify that :func:`magnitude_spectrum` returns a flat spectrum.
   - Create delayed spikes for testing convolution and delay estimation.

   :param n: Number of samples.
   :param amplitude: Value of the spike (e.g. 1.0 for unit impulse).
   :param position: Sample index of the spike (0-based, must be < *n*).

.. autofunction:: pyminidsp.chirp_linear

   Generate a linear chirp (swept sine with linearly increasing
   frequency):

   .. math::

      f(t) = f_\text{start} + (f_\text{end} - f_\text{start}) \cdot t / T

   A linear chirp is the standard test signal for spectrograms — its
   instantaneous frequency traces a straight diagonal line in the
   time-frequency plane.

   :param n: Number of samples.
   :param amplitude: Peak amplitude.
   :param f_start: Starting frequency in Hz.
   :param f_end: Ending frequency in Hz.
   :param sample_rate: Sampling rate in Hz.

   .. code-block:: python

      # 1-second linear chirp from 200 Hz to 4 kHz at 16 kHz
      chirp = md.chirp_linear(16000, f_start=200.0, f_end=4000.0, sample_rate=16000.0)

.. autofunction:: pyminidsp.chirp_log

   Generate a logarithmic chirp (exponentially increasing frequency):

   .. math::

      f(t) = f_\text{start} \cdot (f_\text{end} / f_\text{start})^{t / T}

   Spends equal time per octave, making it ideal for measuring systems
   whose behaviour is best described on a log-frequency axis (e.g. audio
   equaliser response).

   :param n: Number of samples.
   :param amplitude: Peak amplitude.
   :param f_start: Starting frequency in Hz (must be > 0).
   :param f_end: Ending frequency in Hz (must be > 0, ≠ *f_start*).
   :param sample_rate: Sampling rate in Hz.

.. autofunction:: pyminidsp.square_wave

   Generate a bipolar square wave that alternates between +amplitude
   and −amplitude.

   Contains only **odd harmonics** (1f, 3f, 5f, …) whose amplitudes
   decay as 1/k — a classic demonstration of the Fourier series and
   the Gibbs phenomenon.

.. autofunction:: pyminidsp.sawtooth_wave

   Generate a sawtooth wave that ramps linearly from −amplitude to
   +amplitude over each period.

   Contains **all integer harmonics** (1f, 2f, 3f, …) decaying as 1/k
   — richer harmonic content compared to the square wave.

.. autofunction:: pyminidsp.shepard_tone

   Generate a `Shepard tone <https://en.wikipedia.org/wiki/Shepard_tone>`_
   — the auditory illusion of endlessly rising or falling pitch.

   Superimposes several sine waves spaced one octave apart.  Each tone
   glides continuously in pitch while a Gaussian spectral envelope — fixed
   in log-frequency space — fades tones in at one end and out at the other.

   .. math::

      x[n] = A_\text{norm}\sum_k
        \exp\!\left(-\frac{d_k(t)^2}{2\sigma^2}\right)
        \sin(\varphi_k(n))

   :param n: Number of samples.
   :param amplitude: Peak amplitude.
   :param base_freq: Centre frequency of the Gaussian envelope (typical: 200–600 Hz).
   :param sample_rate: Sampling rate in Hz.
   :param rate_octaves_per_sec: Glissando rate (positive = rising, negative = falling,
                                 0 = static chord).
   :param num_octaves: Number of audible octave layers (typical: 6–10).

   .. code-block:: python

      # 5 seconds of endlessly rising Shepard tone
      sig = md.shepard_tone(5 * 44100, amplitude=0.8, base_freq=440.0,
                             sample_rate=44100.0, rate_octaves_per_sec=0.5)
