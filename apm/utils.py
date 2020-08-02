"""Utility functions for the aperiodic methods project."""

import numpy as np

from apm.core.utils import _check1D, _check2D

###################################################################################################
###################################################################################################

def abs_err(val, fit):
    """Absolute error of fit."""

    return abs(val - fit)


def sqd_err(val, fit):
    """Squared error of fit."""

    return (val - fit) ** 2


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
