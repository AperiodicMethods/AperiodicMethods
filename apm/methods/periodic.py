"""Periodic measurement functions."""

import warnings

import numpy as np

# Ignore deprecation / update warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    from fooof import FOOOF
    from fooof.utils import trim_spectrum
from neurodsp.spectral import compute_spectrum

from apm.methods.settings import ALPHA_RANGE

###################################################################################################
###################################################################################################

def alpha_power(sig, log=True, **kwargs):
    """Wrapper function for applying specparam and extracting alpha power."""

    freqs, powers = compute_spectrum(sig, kwargs.pop('fs'), f_range=kwargs.pop('f_range', None))

    if 'fm' in kwargs:
        fm = kwargs.pop('fm')
    else:
        fm = FOOOF(**kwargs, verbose=False)

    fm.fit(freqs, powers)

    alpha_power = get_fm_peak_power(fm, ALPHA_RANGE, log=log)

    return alpha_power


def get_fm_peak_power(fm, peak_range, log=True):
    """Helper function for getting peak power from spectral model."""

    peak_freqs, peak_powers = trim_spectrum(\
        fm.freqs, fm.get_data('peak', 'linear'), peak_range)

    peak_power = np.max(peak_powers)

    if log:
        peak_power = np.log10(peak_power)

    return peak_power
