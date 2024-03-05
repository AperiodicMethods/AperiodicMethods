"""Simulation utilities."""

from itertools import count

###################################################################################################
###################################################################################################

def counter(value):
    """Counter that supports both finite and infinite ranges.

    Parameters
    ----------
    value : int or None
        Upper bound for the counter (if finite) or None (if infinite).

    Returns
    -------
    counter : range or count
        Counter object for finite (range) or infinite (count) iteration.
    """

    return range(value) if value else count()
