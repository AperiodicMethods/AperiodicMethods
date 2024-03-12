"""Wrapper functions to create a consistent API for running measures of aperiodic activity."""

import warnings

import numpy as np
from scipy.optimize import curve_fit

from antropy import hjorth_params, lziv_complexity
from neurokit2.complexity import (fractal_correlation, fractal_sevcik, complexity_lyapunov,
                                  complexity_wpe, entropy_multiscale)

from fooof import FOOOF
from fooof.core.funcs import expo_function
from fooof.core.errors import NoModelError

from neurodsp.spectral import compute_spectrum
from neurodsp.aperiodic.dfa import compute_fluctuations
from neurodsp.aperiodic.autocorr import compute_autocorr
from neurodsp.aperiodic.irasa import compute_irasa, fit_irasa

# Import local autocorrelation functions
from apm.methods.ac import compute_decay_time, fit_acf

###################################################################################################
###################################################################################################

## AUTOCORRELATION MEASURES

def autocorr(sig, **kwargs):
    """Wrapper funtion for computing autocorrelation."""

    return compute_autocorr(sig, **kwargs)[1]


def autocorr_decay_time(sig, fs, level=0, **kwargs):
    """Wrapper function for computing the autocorrelation & decay time together."""

    return compute_decay_time(*compute_autocorr(sig, **kwargs), fs, level)


def autocorr_timescale(sig, fs, **kwargs):
    """Wrapper function for computing autocorrelation and timescale together."""

    return fit_acf(*compute_autocorr(sig, **kwargs), fs)[0]


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


def lyapunov(sig, **kwargs):
    """Wrapper function for computing Lyapunov exponent."""

    return complexity_lyapunov(sig)[0]


## FRACTAL DIMENSION MEASURES

def correlation_dimension(sig, **kwargs):
    """Wrapper function for computing correlation dimension."""

    return fractal_correlation(sig, **kwargs)[0]


def sevcik_fd(sig, **kwargs):
    """Wrapper function for computing Sevcik fractal dimension."""

    return fractal_sevcik(sig)[0]


## ENTROPY MEASURES

def wperm_entropy(sig, **kwargs):
    """Wrapper function for computing weighted permutation entropy."""

    return complexity_wpe(sig, **kwargs)[0]


## MULTISCALE ENTROPY MEASURES

def multi_app_entropy(sig, **kwargs):
    """Wrapper function for computing multiscale approximate entropy."""

    return entropy_multiscale(sig, method='MSApEn', **kwargs)[0]


def multi_sample_entropy(sig, **kwargs):
    """Wrapper function for computing multiscale sample entropy."""

    return entropy_multiscale(sig, method='MSEn', **kwargs)[0]


def multi_perm_entropy(sig, **kwargs):
    """Wrapper function for computing multiscale permutation entropy."""

    return entropy_multiscale(sig, method='MSPEn', **kwargs)[0]


def multi_wperm_entropy(sig, **kwargs):
    """Wrapper function for computing multiscale weighted permutation entropy."""

    return entropy_multiscale(sig, method='MSWPEn', **kwargs)[0]

## SPECTRAL MEASURES

def fit_irasa_exp(freqs, psd_ap):
    """IRASAS fit function - fit single exponent model & return exponent."""

    return fit_irasa(freqs, psd_ap)[1]


def fit_irasa_knee(freqs, psd_ap):
    """IRASA fit function - fit knee model."""

    # Force non-negative parameters
    lower_bounds = (0, 0, 0)
    upper_bounds = (np.inf, np.inf, np.inf)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        popt, _ = curve_fit(expo_function, freqs, np.log10(psd_ap),
                            p0=(0, 0, 0), maxfev=5000)
    offset, knee, exp = popt

    return offset, knee, -exp


def fit_irasa_knee_exp(freqs, psd_ap):
    """IRASA fit function - fit knee model & return exponent."""

    return fit_irasa_knee(freqs, psd_ap)[2]


IRASA_FIT_FUNCS = {
    'fit_irasa_exp' : fit_irasa_exp,
    'fit_irasa_knee' : fit_irasa_knee_exp,
}


def irasa(sig, fit_func='fit_irasa_exp', flip_sign=True, **kwargs):
    """Wrapper function for fitting IRASA and returning fit exponent.

    Note: output value is sign-flipped, to match specparam format.
    """

    freqs, psd_ap, psd_pe = compute_irasa(sig, **kwargs)

    try:
        exponent = IRASA_FIT_FUNCS[fit_func](freqs, psd_ap)
    except RuntimeError:
        exponent = np.nan

    if flip_sign:
        exponent = -1 * exponent

    return exponent


def specparam(sig, **kwargs):
    """Wrapper function for applying specparam (starting from a time series)."""

    freqs, powers = compute_spectrum(sig, kwargs.pop('fs'), f_range=kwargs.pop('f_range', None))

    if 'fm' in kwargs:
        fm = kwargs.pop('fm')
    else:
        fm = FOOOF(**kwargs, verbose=False)

    fm.fit(freqs, powers)

    try:
        exponent = fm.get_params('aperiodic', 'exponent')
    except NoModelError:
        exponent = np.nan

    return exponent
