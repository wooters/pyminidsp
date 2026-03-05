Signal Scaling
==============

Functions for mapping values between ranges and automatic gain control.

.. autofunction:: pyminidsp.scale

   Map a single value from one range to another.

   Example: ``scale(5.0, 0.0, 10.0, 0.0, 100.0)`` returns ``50.0``.

.. autofunction:: pyminidsp.scale_vec

   Map every element of a vector from one range to another.

.. autofunction:: pyminidsp.fit_within_range

   Fit values within ``[newmin, newmax]``.  If all values already fit,
   they are copied unchanged.  Otherwise the entire vector is rescaled.

.. autofunction:: pyminidsp.adjust_dblevel

   Automatic Gain Control: scale a signal so its power matches
   the requested dB level, then clip to [-1, 1].
