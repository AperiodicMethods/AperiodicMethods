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

def alpha_power(sig, **kwargs):
    """Wrapper function for applying specparam and extracting alpha power."""

    freqs, powers = compute_spectrum(sig, kwargs.pop('fs'), f_range=kwargs.pop('f_range', None))

    if 'fm' in kwargs:
        fm = kwargs.pop('fm')
    else:
        fm = FOOOF(**kwargs, verbose=False)

    fm.fit(freqs, powers)
    alpha_freqs, alpha_powers = trim_spectrum(fm.freqs, fm.get_data('peak', 'linear'), ALPHA_RANGE)

    alpha_peak = np.max(alpha_powers)

    return alpha_peak
