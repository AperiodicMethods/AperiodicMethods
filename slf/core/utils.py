"""Utilities for slope fitting project."""

import numpy as np

################################################################################
################################################################################

def extract_psd(freqs, psd, f_low, f_high):
    """Extract frequency range of interest from PSD data.

    Parameters
    ----------
    freqs : ?
        xx
    psd : ?
        xx
    f_low : ?
        xx
    f_high : ?
        xx

    Returns
    -------
    freqs_out : ?
        xx
    psd_out : ?
        xx
    """

    # Boolean indexing needs to be array - not list
    if isinstance(freqs, list):
        freqs = np.array(freqs)

    # Drop frequencies below f_low
    f_low_mask = freqs >= f_low
    freqs_ext = freqs[f_low_mask]
    psd_ext = psd[f_low_mask]

    # Drop frequencies above f_high
    f_high_mask = freqs_ext <= f_high
    freqs_ext = freqs_ext[f_high_mask]
    psd_ext = _check(psd_ext[f_high_mask])

    return freqs_ext, psd_ext


def exclude_psd(freqs, psd, exclude):
    """Drop an exclusion range of frequencies.

    Parameters
    ----------
    freqs : ?
        xx
    psd : ?
        xx
    exclude : ?
        xx

    Returns
    -------
    freqs_out : ?
        xx
    psd_out : ?
        xx
    """

    f_mask = np.array([(a or b) for a, b in zip(freqs < exclude[0],
                                                freqs > exclude[1])])

    freqs_out = _check(freqs[f_mask])
    psd_out = _check(psd[f_mask])

    return freqs_out, psd_out

################################################################################
################################################################################

def CheckDims(func):
    """Decorator function to check all inputs are 2-D."""

    def wrapper(*args):
        args = [_check(arg) for arg in args]
        return func(*args)

    return wrapper

################################################################################
################################################################################

def _check(arr):
    """Check that array is 2-D, reshape if not."""

    if arr.ndim == 1:
        return arr.reshape([len(arr), 1])
    else:
        return arr
