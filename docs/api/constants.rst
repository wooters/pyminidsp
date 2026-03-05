Constants
=========

Filter types
------------

.. data:: pyminidsp.LPF

   Low-pass filter (0).

.. data:: pyminidsp.HPF

   High-pass filter (1).

.. data:: pyminidsp.BPF

   Band-pass filter (2).

.. data:: pyminidsp.NOTCH

   Notch filter (3).

.. data:: pyminidsp.PEQ

   Peaking EQ (4).

.. data:: pyminidsp.LSH

   Low shelf (5).

.. data:: pyminidsp.HSH

   High shelf (6).


Steganography methods
---------------------

.. data:: pyminidsp.STEG_LSB

   Least-significant-bit encoding (0).

.. data:: pyminidsp.STEG_FREQ_BAND

   Near-ultrasonic frequency-band modulation / BFSK (1).

.. data:: pyminidsp.STEG_TYPE_TEXT

   Payload type: text / null-terminated string (0).

.. data:: pyminidsp.STEG_TYPE_BINARY

   Payload type: binary / raw bytes (1).


GCC weighting types
-------------------

.. data:: pyminidsp.GCC_SIMP

   Simple 1/N weighting — basic cross-correlation (0).

.. data:: pyminidsp.GCC_PHAT

   Phase Transform weighting — sharper peaks, more robust to noise (1).


Cleanup
-------

.. autofunction:: pyminidsp.shutdown

   Free all internally cached FFT plans and buffers.  Registered with
   :mod:`atexit` so it runs automatically at interpreter exit, but can
   be called explicitly to free memory sooner.
