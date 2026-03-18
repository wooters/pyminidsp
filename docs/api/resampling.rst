Resampling
==========

Sample rate conversion using a polyphase sinc resampler with
Kaiser-windowed anti-aliasing filter.

.. autofunction:: pyminidsp.resample_output_len

   Compute the number of output samples for a given resampling operation.
   Use this to pre-allocate buffers when you need fine control over memory.

   :param input_len: Number of input samples.
   :param in_rate: Input sample rate in Hz.
   :param out_rate: Output sample rate in Hz.
   :returns: Number of output samples.

.. autofunction:: pyminidsp.resample

   Resample a signal using a polyphase sinc resampler.  Automatically
   computes the output buffer size and applies a Kaiser-windowed
   anti-aliasing filter to prevent aliasing during downsampling.

   :param signal: Input signal.
   :param in_rate: Input sample rate in Hz.
   :param out_rate: Output sample rate in Hz.
   :param num_zero_crossings: Number of zero crossings in the sinc kernel (default 13).
   :param kaiser_beta: Kaiser window shape parameter (default 5.0).
   :returns: Resampled signal array.

   .. code-block:: python

      # Upsample from 22050 Hz to 44100 Hz
      signal = md.sine_wave(22050, freq=440.0, sample_rate=22050.0)
      upsampled = md.resample(signal, in_rate=22050.0, out_rate=44100.0)
      # len(upsampled) == 44100

      # Downsample from 48000 Hz to 16000 Hz
      signal = md.sine_wave(48000, freq=440.0, sample_rate=48000.0)
      downsampled = md.resample(signal, in_rate=48000.0, out_rate=16000.0)
