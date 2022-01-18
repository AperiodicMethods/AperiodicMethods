"""Wrapper functions for measure functions for running them across simulations."""

import numpy as np

from antropy import hjorth_params

from fooof import FOOOF

from neurodsp.spectral import compute_spectrum
from neurodsp.aperiodic.dfa import compute_fluctuations
from neurodsp.aperiodic.autocorr import compute_autocorr
from neurodsp.aperiodic.irasa import compute_irasa, fit_irasa

###################################################################################################
###################################################################################################

def autocorr_wrapper(sig, **kwargs):
    """Wrapper funtion for computing autocorrelation."""

    return compute_autocorr(sig, **kwargs)[1]


def hurst_wrapper(sig, **kwargs):
    """Wrapper function for computing the Hurst exponent."""

    return compute_fluctuations(sig, method='rs', **kwargs)[2]


def dfa_wrapper(sig, **kwargs):
    """Wrapper function for computing DFA."""

    return compute_fluctuations(sig, method='dfa', **kwargs)[2]


def hjorth_activity_wrapper(sig):
    """Wrapper function for computing Hjorth activity.
    Note: 'Hjorth activity' is the variance of the signal.
    """

    return np.var(sig)


def hjorth_mobility_wrapper(sig):
    """Wrapper function for computing Hjorth mobility."""

    return hjorth_params(sig)[0]


def hjorth_complexity_wrapper(sig):
    """Wrapper function for computing Hjorth complexity."""

    return hjorth_params(sig)[1]


def lempelziv_wrapper(sig, **kwargs):
    """Wrapper function for computing Lempel-Ziv complexity.
    Note: LZ complexity is computed on a binarized version of the signal."""

    bin_sig = np.array(sig > np.median(sig)).astype(int)
    return lziv_complexity(bin_sig, **kwargs)


def irasa_wrapper(sig, **kwargs):
    """Wrapper function for fitting IRASA and returning fit exponent."""

    freqs, psd_ap, psd_pe = compute_irasa(sig, **kwargs)
    return fit_irasa(freqs, psd_ap)[1]


def specparam_wrapper(sig, **kwargs):
    """Wrapper function for applying spec-param (starting from a time series)."""

    freqs, powers = compute_spectrum(sig, kwargs.pop('fs'), f_range=kwargs.pop('f_range', None))
    fm = FOOOF(**kwargs, verbose=False)
    fm.fit(freqs, powers)
    return fm.get_params('aperiodic', 'exponent')
