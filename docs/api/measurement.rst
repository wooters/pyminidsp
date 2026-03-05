Signal Measurement
==================

Basic time-domain metrics for characterising a signal's amplitude,
energy, and information content.

.. autofunction:: pyminidsp.dot

   Compute the dot product of two vectors: the sum of element-wise
   products ``a[0]*b[0] + a[1]*b[1] + ...``

   If the arrays differ in length, only the first ``min(len(a), len(b))``
   elements are used.

.. autofunction:: pyminidsp.entropy

   Returns a value between 0.0 (all energy concentrated in one bin)
   and 1.0 (energy spread equally across all bins).

   :param a: Input distribution.
   :param clip: If ``True``, ignore negative values.
                If ``False``, square all values first.
   :rtype: float

.. autofunction:: pyminidsp.energy

   Compute signal energy: sum of squared samples.

   .. math::

      E = \sum_{n=0}^{N-1} x[n]^2

.. autofunction:: pyminidsp.power

   Compute signal power: energy divided by the number of samples.

   .. math::

      P = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2

.. autofunction:: pyminidsp.power_db

   Compute signal power in decibels: ``10 * log10(power)``.
