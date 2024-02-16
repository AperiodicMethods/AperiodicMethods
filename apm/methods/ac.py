"""Autocorrelation relation functionality.

Note: this is to be checked and likely moved into neurodsp.
"""

import numpy as np
from scipy.optimize import curve_fit

###################################################################################################
###################################################################################################

def compute_decay_time(times, acs, fs, level=0):
    """Compute autocorrelation decay time, from precomputed autocorrelation.

    Parameters
    ----------
    times : 1d array
        Timepoints for the computed autocorrelations.
    acs : 1d array
        Autocorrelation values.
    fs : int
        Sampling rate of the signal.
    level : float
        Autocorrelation decay threshold.

    Returns
    -------
    result : float
        Autocorrelation decay time.

    Notes
    -----
    The autocorrelation decay time is computed as the time delay for the autocorrelation
    to drop to (or below) the decay time threshold.
    """

    val_checks = acs <= level

    if np.any(val_checks):
        # Get the first value to cross the threshold, and convert to time value
        result = times[np.argmax(val_checks)] / fs
    else:
        result = np.nan

    return result


### Functions for fitting Autocorrelation
def exp_decay_func(times, tau, A, B):
    """Exponential decay fit function.

    Parameters
    ----------
    times : 1d array
        Time values.
    tau : float
        Timescale value.
    A : float
        Scaling factor, which captures the start value of the function.
    B : float
        Offset factor, which captures the end value of the function.
    """

    return A * (np.exp(-times / tau) + B)


def exp_delay_double_func(times, tau1, tau2, A1, A2, B):
    """Exponential decay fit funtion with two timescales.

    Parameters
    ----------
    times : 1d array
        Time values.
    tau1, tau2 : float
        Timescale values, for the 1st and 2nd timescale.
    A1, A2 : float
        Scaling factors, for the 1st and 2nd timescale.
    B : float
        Offset factor.
    """

    return A1 * np.exp(-times / tau1) + A2 * np.exp(-times / tau2) + B


def fit_acf(times, acs, fs=None):
    """Fit autocorrelation function, returning timescale estimate.

    Parameters
    ----------
    times : 1d array
        Timepoints for the computed autocorrelations.
    acs : 1d array
        Autocorrelation values.
    fs : int, optional
        Sampling rate of the signal.

    Returns
    -------
    popts
        Fit parameters.
    """

    if fs:
        times = times / fs

    p_bounds =([0, 0, 0], [10, np.inf, np.inf])
    popts, _ = curve_fit(exp_decay_func, times, acs, bounds=p_bounds)

    return popts


def regen_exp_values(times, *popts):
    """Regenerate values of the exponential decay fit."""

    return exp_decay_func(times, *popts)
