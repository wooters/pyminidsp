Spectral Analysis
=================

FFT-based frequency-domain analysis: magnitude spectrum, power spectral
density, phase spectrum, STFT, mel filterbanks, and MFCCs.

.. autofunction:: pyminidsp.magnitude_spectrum

   Compute the magnitude spectrum of a real-valued signal.

   Given a signal of length *N*, computes the FFT and returns
   ``|X(k)|`` for each frequency bin.  Because the input is real-valued,
   only the first ``N/2 + 1`` bins are unique (from DC through Nyquist).

   To convert bin index *k* to a frequency in Hz::

      freq_k = k * sample_rate / N

   The output is **not** normalised by *N*.  Divide each value by *N*
   for the standard DFT magnitude, or by ``N/2`` (except DC and Nyquist)
   for single-sided amplitude.

   :param signal: Input signal.
   :returns: Array of length ``N // 2 + 1``.

   .. code-block:: python

      signal = md.sine_wave(1024, freq=440.0, sample_rate=44100.0)
      mag = md.magnitude_spectrum(signal)
      # mag[0]   = DC component magnitude
      # mag[k]   = magnitude at frequency k * 44100 / 1024
      # mag[512] = Nyquist frequency magnitude

.. autofunction:: pyminidsp.power_spectral_density

   Compute the power spectral density (PSD) — the periodogram estimator:

   .. math::

      \text{PSD}[k] = \frac{|X(k)|^2}{N}

   While the magnitude spectrum tells you the *amplitude* at each
   frequency, the PSD tells you the *power* — useful for noise analysis,
   SNR estimation, and comparing signals of different lengths.

   **Parseval's theorem** (energy conservation):
   ``PSD[0] + 2 * sum(PSD[1:N//2]) + PSD[N//2] == sum(x[n]**2)``

   :param signal: Input signal.
   :returns: Array of length ``N // 2 + 1``.

.. autofunction:: pyminidsp.phase_spectrum

   Compute the one-sided phase spectrum in radians.

   Returns the instantaneous phase angle
   :math:`\phi(k) = \arg X(k)` for each DFT bin, in the range
   :math:`[-\pi, \pi]`.

   **Interpretation:**

   - A pure cosine at an integer bin produces :math:`\phi = 0`.
   - A pure sine at the same bin produces :math:`\phi = -\pi/2`.
   - A time-delayed signal exhibits **linear phase**:
     :math:`\phi(k) = -2\pi k d / N` where *d* is the delay in samples.

   .. note::

      Phase values at bins where the magnitude is near zero are
      numerically unreliable.  Always examine :func:`magnitude_spectrum`
      alongside the phase spectrum to identify significant bins.

   :param signal: Input signal.
   :returns: Array of length ``N // 2 + 1``, values in :math:`[-\pi, \pi]`.

.. autofunction:: pyminidsp.stft_num_frames

   Compute the number of STFT frames::

      num_frames = (signal_len - n) // hop + 1   when signal_len >= n
      num_frames = 0                              when signal_len < n

   Use this to predict the shape of :func:`stft` output.

.. autofunction:: pyminidsp.stft

   Compute the Short-Time Fourier Transform (STFT).

   Slides a Hanning-windowed FFT over the signal in steps of *hop*
   samples, producing a time-frequency magnitude matrix.  For each
   frame, the function applies a Hanning window, computes the FFT,
   and stores ``|X(k)|`` for bins ``0..N//2``.

   The output is **not** normalised by *N* — divide each value by *N*
   for standard DFT magnitude.

   :param signal: Input signal.
   :param n: FFT window size (must be >= 2).
   :param hop: Hop size in samples (must be >= 1).
   :returns: 2D array of shape ``(num_frames, n // 2 + 1)``.

   .. code-block:: python

      signal = md.sine_wave(16000, freq=440.0, sample_rate=16000.0)
      spec = md.stft(signal, n=512, hop=128)
      # spec.shape == (num_frames, 257)
      # Convert bin k to Hz: freq_hz = k * sample_rate / n
      # Convert frame f to seconds: time_s = f * hop / sample_rate

.. autofunction:: pyminidsp.mel_filterbank

   Build a mel-spaced triangular filterbank matrix using the HTK mel
   mapping:

   .. math::

      \text{mel}(f) = 2595 \cdot \log_{10}\!\left(1 + \frac{f}{700}\right)

   :param n: FFT size (must be >= 2).
   :param sample_rate: Sampling rate in Hz.
   :param num_mels: Number of mel filters.
   :param min_freq_hz: Lower frequency bound in Hz.
   :param max_freq_hz: Upper frequency bound (defaults to ``sample_rate / 2``).
   :returns: 2D array of shape ``(num_mels, n // 2 + 1)``.

.. autofunction:: pyminidsp.mel_energies

   Compute mel-band energies from a single frame.

   Processing steps: (1) apply an internal Hann window, (2) compute
   one-sided PSD bins via FFT, (3) apply mel filterbank weights and
   sum per band.

   :param signal: Input frame.
   :param sample_rate: Sampling rate in Hz.
   :param num_mels: Number of mel bands.
   :param min_freq_hz: Lower frequency bound.
   :param max_freq_hz: Upper frequency bound (defaults to ``sample_rate / 2``).
   :returns: Array of length *num_mels*.

.. autofunction:: pyminidsp.mfcc

   Compute mel-frequency cepstral coefficients (MFCCs) from a single
   frame.

   Conventions:

   - HTK mel mapping for filter placement.
   - Internal Hann windowing and one-sided PSD mel energies.
   - Natural-log compression: ``log(max(E_mel, 1e-12))``.
   - DCT-II with HTK-C0 profile:
     ``c0`` uses ``sqrt(1/M)`` normalisation,
     ``c_n`` (n > 0) uses ``sqrt(2/M)``, where M = *num_mels*.
   - Coefficient C0 is written to ``mfcc_out[0]``.

   :param signal: Input frame.
   :param sample_rate: Sampling rate in Hz.
   :param num_mels: Number of mel bands.
   :param num_coeffs: Number of cepstral coefficients (must be in ``[1, num_mels]``).
   :param min_freq_hz: Lower frequency bound.
   :param max_freq_hz: Upper frequency bound (defaults to ``sample_rate / 2``).
   :returns: Array of length *num_coeffs*.

   .. code-block:: python

      signal = md.sine_wave(512, freq=440.0, sample_rate=16000.0)
      coeffs = md.mfcc(signal, sample_rate=16000.0, num_mels=26, num_coeffs=13)
