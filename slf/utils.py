import numpy as np

################################################################################
################################################################################

def extract_psd(psd, freqs, f_low, f_high):
    """Extract frequency range of interest from PSD data."""

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

    return psd_ext, freqs_ext

def exclude_psd(psd, freqs, exclude):
    """Drop an exclusion range of frequencies."""

    f_mask = np.array([(a or b) for a, b in zip(freqs < exclude[0],
                                                freqs > exclude[1])])

    freqs_out = _check(freqs[f_mask])
    psd_out = _check(psd[f_mask])

    return psd_out, freqs_out

################################################################################
################################################################################

def _check(arr):
    """Check that array is 2-D, reshape if not."""

    if arr.ndim == 1: return arr.reshape([len(arr), 1])
    else: return arr
