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


def print_results(data):
    """Print out the mean errors per method.

    Parameters
    ----------
    data : list of tuple
        List with each element containing (float, string).
    """

    for it in data:
        print('   {:8} \t\t {:1.5f}'.format(it[1], it[0]))


def format_corr(r_val, p_val, cis):
    """Format correlation results for printing."""

    return 'r={:+1.3f}  CI[{:+1.3f}, {:+1.3f}],  p={:1.3f}'.format(r_val, *cis, p_val)


def sampler(values, probs=None):
    """Create a generator to sample from a parameter range."""

    # Check that length of options is same as length of probs, if provided
    if np.any(probs):
        if len(inds) != len(probs):
            raise ValueError("The number of options must match the number of probabilities.")

    while True:
        yield np.random.choice(values, p=probs)
