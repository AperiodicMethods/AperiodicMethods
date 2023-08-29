"""Wrapper functions for measure functions for running them across simulations."""

import numpy as np

from antropy import hjorth_params, lziv_complexity

from fooof import FOOOF

from neurodsp.spectral import compute_spectrum
from neurodsp.aperiodic.dfa import compute_fluctuations
from neurodsp.aperiodic.autocorr import compute_autocorr
from neurodsp.aperiodic.irasa import compute_irasa, fit_irasa

###################################################################################################
###################################################################################################

## AUTOCORRELATION MEASURES

def autocorr(sig, **kwargs):
    """Wrapper funtion for computing autocorrelation."""

    return compute_autocorr(sig, **kwargs)[1]


def autocorr_decay_time(sig, fs, level=0, **kwargs):
    """Wrapper function for computing the autocorrelation & decay time together."""

    return compute_decay_time(*compute_autocorr(sig, **kwargs), fs, level)


def compute_decay_time(times, acs, fs, level=0):
    """Compute autocorrelation decay time, from precomputed autocorrelation.
    Note: this could be added to NDSP?
    """

    val_checks = acs < level

    if np.any(val_checks):
        result = times[np.argmax(val_checks)] / fs
    else:
        result = np.nan

    return result

## FLUCTUATION MEASURES

def hurst(sig, **kwargs):
    """Wrapper function for computing the Hurst exponent."""

    return compute_fluctuations(sig, method='rs', **kwargs)[2]


def dfa(sig, **kwargs):
    """Wrapper function for computing DFA."""

    return compute_fluctuations(sig, method='dfa', **kwargs)[2]


## COMPLEXITY MEASURES

def hjorth_activity(sig):
    """Wrapper function for computing Hjorth activity.
    Note: 'Hjorth activity' is the variance of the signal.
    """

    return np.var(sig)


def hjorth_mobility(sig):
    """Wrapper function for computing Hjorth mobility."""

    return hjorth_params(sig)[0]


def hjorth_complexity(sig):
    """Wrapper function for computing Hjorth complexity."""

    return hjorth_params(sig)[1]


def lempelziv(sig, **kwargs):
    """Wrapper function for computing Lempel-Ziv complexity.
    Note: LZ complexity is computed on a binarized version of the signal."""

    bin_sig = np.array(sig > np.median(sig)).astype(int)
    return lziv_complexity(bin_sig, **kwargs)

## SPECTRAL MEASURES

def irasa(sig, **kwargs):
    """Wrapper function for fitting IRASA and returning fit exponent."""

    freqs, psd_ap, psd_pe = compute_irasa(sig, **kwargs)
    return fit_irasa(freqs, psd_ap)[1]


def specparam(sig, **kwargs):
    """Wrapper function for applying spec-param (starting from a time series)."""

    freqs, powers = compute_spectrum(sig, kwargs.pop('fs'), f_range=kwargs.pop('f_range', None))
    fm = FOOOF(**kwargs, verbose=False)
    fm.fit(freqs, powers)
    return fm.get_params('aperiodic', 'exponent')
