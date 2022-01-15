"""Wrapper functions that wrap measure functions to assist with running them across simulations."""

from antropy import hjorth_params

from neurodsp.aperiodic.dfa import compute_fluctuations
from neurodsp.aperiodic.autocorr import compute_autocorr
from neurodsp.aperiodic.irasa import compute_irasa, fit_irasa

###################################################################################################
###################################################################################################

def autocorr_wrapper(sig, **kwargs):
    """Wrapper funtion for computing autocorrelation."""

    return compute_autocorr(sig, **kwargs)[1]


def hurst_wrapper(sig, **kwargs):
    """Wrapper function for computing and getting Hurst exponent."""

    return compute_fluctuations(sig, method='rs', **kwargs)[2]


def dfa_wrapper(sig, **kwargs):
    """Wrapper function for computing and returing DFA measure."""

    return compute_fluctuations(sig, method='dfa', **kwargs)[2]


def hjorth_mobility_wrapper(sig):
    """Wrapper function for computing Hjorth mobility."""

    return hjorth_params(sig)[0]


def hjorth_complexity_wrapper(sig):
    """Wrapper function for computing Hjorth complexity."""

    return hjorth_params(sig)[1]


def irasa_wrapper(sig, **kwargs):
    """Wrapper function for fitting IRASA and returning fit exponent."""

    freqs, psd_ap, psd_pe = compute_irasa(sig, **irasa_params)
    return fit_irasa(freqs, psd_ap)[1]
