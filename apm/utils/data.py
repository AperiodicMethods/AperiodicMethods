"""Utilities for working with data."""

import numpy as np

from apm.utils.decorators import _check1D, _check2D

###################################################################################################
###################################################################################################

def exclude_spectrum(freqs, spectrum, exclude, make_2D=True):
    """Drop an exclusion range of frequencies from a spectrum."""

    f_mask = np.array([(aa or bb) for aa, bb in zip(freqs < exclude[0], freqs > exclude[1])])

    if make_2D:
        freqs_out = _check2D(freqs[f_mask])
        spectrum_out = _check2D(spectrum[f_mask])
    else:
        freqs_out = _check1D(freqs[f_mask])
        spectrum_out = _check1D(spectrum[f_mask])

    return freqs_out, spectrum_out


def min_n_max(array, absolute=True):
    """Get the min and max value of an array"""

    if absolute:
        array = np.abs(array)

    return min(array), max(array)


def select_vals(select, *arrays):
    """Select specified values from a set of arrays.

    Parameters
    ----------
    select : 1d array of bool
        Mask to select from arrays.
    *arrays
        Arrays to select from.
    """

    if select is not None:
        arrays = [arr[select] for arr in arrays]

    return arrays
